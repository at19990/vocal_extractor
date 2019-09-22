#!/usr/bin/env python
# coding: utf-8

"""
ボーカル入りの楽曲とカラオケ音源からボーカルを抽出するプログラムです
16bit, サンプリング周波数 44.1kHz のwav形式を処理可能です
コマンドで、
> python vocal_extract.py {元楽曲ファイル名} {カラオケ音源ファイル名} {出力ファイル名} {楽曲の先頭探索のしきい値(0.01~0.1を推奨)}
のように入力すると実行できます
元音源とカラオケ音源の開始タイミングが極端にずれているものや、
前奏がなく始まる楽曲では抽出を行えない可能性があります
"""

import sys
import soundfile as sf


# 引数の数が合致しないとき、ヘルプを表示して終了
def display_help():
    print("[HELP] vocal_extract.py {mixed_file_name} {inst_file_name} "
          "{output_file_name} {threshold(0.01~0.1 recommended)}")
    print("This program only accepts wav file.")
    sys.exit(0)


 # データ長を検証
def arrange_data_length(wav_mixed, wav_kara):
    if len(wav_mixed) >= len(wav_kara):
        return len(wav_kara)
    else:
        return len(wav_mixed)


# 楽曲の開始点の検証(先頭10秒まで)
def detect_start_mixed(wav_mixed, param):
    for i in range(441000):
        if wav_mixed[i, 0] >= param:
            return i


# カラオケの開始点の検証(先頭10秒まで)
def detect_start_kara(wav_kara, param):
    for j in range(441000):
        if wav_kara[j, 0] >= param:
            return j


# 位相を反転してぶつける
def compound_opposite_phase(wav_mixed_head, wav_kara_head, t, length):
    if t <= 1.0:
        return wav_mixed_head[0:length, :] + (-1) * t * wav_kara_head[0:length, :]
    else:
        return wav_mixed_head[0:length, :] * (1/t) + (-1) * wav_kara_head[0:length, :]


# 音割れを除去
# 入れ子にするとかなり遅くなったので左右のチャンネルで処理を分割
def remove_clipping(wav_vo):
    length_vo = len(wav_vo)
    for i in range(length_vo):
        if wav_vo[i, 0] > 1:
            wav_vo[i, 0] = 1
        if wav_vo[i, 1] > 1:
            wav_vo[i, 1] = 1
    return wav_vo


def main():
    # コマンド引数を取得
    args = sys.argv

    if len(args) != 5:
        display_help()

    mixed_file_name = args[1]
    kara_file_name = args[2]
    output_file_name = args[3]
    param = float(args[4])

    wav_mixed, fs1 = sf.read(mixed_file_name)
    wav_kara, fs2 = sf.read(kara_file_name)

    length = arrange_data_length(wav_mixed, wav_kara)

    st_mixed = detect_start_mixed(wav_mixed, param)
    st_kara = detect_start_kara(wav_kara, param)

    # 頭出しして長さをそろえる
    # → この部分は試しているうちに半ば偶然うまく動作したものなのでもっと簡潔に書けるはず
    wav_mixed_head = wav_mixed[st_mixed: st_mixed + length - st_kara, :]
    wav_kara_head = wav_kara[st_kara: st_kara + length - st_mixed, :]

    if len(wav_mixed_head) > len(wav_kara_head):
        wav_mixed_head = wav_mixed[st_mixed: length, :]
    if len(wav_mixed_head) < len(wav_kara_head):
        wav_kara_head = wav_kara[st_kara: length, :]

    # 各音源の音圧を比較してその倍率を計算
    t = wav_mixed_head[0, 0] / wav_kara_head[0, 0]

    wav_vo = compound_opposite_phase(wav_mixed_head, wav_kara_head, t, length)
    wav_vo = remove_clipping(wav_vo)

    # ファイルに書き出し
    sf.write(output_file_name, wav_vo, fs1)


if __name__ == "__main__":
    main()
