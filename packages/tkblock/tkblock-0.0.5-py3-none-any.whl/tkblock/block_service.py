#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""BlockService

このクラスを使用することでblock指定でwidgetを配置することができる。
"""
from typing import Any

from .canvas import ResizingCanvas
from .block_framebase import BlockFrameBase
from .layout import Layout
from .block_framework import BlockFramework


class BlockService:
    """BlockFrameworkを操作するためのクラス"""

    root = None

    @classmethod
    def init(
        cls, title: str, max_col: int, max_row: int, width: int, height: int
    ) -> BlockFramework:
        """コンストラクタ

        Args:
            title (str): rootのタイトル名
            max_col (int): defaultとなる分割する列数
            max_row (int): defaultとなる分割する行数
            width (int): フレームの横幅
            height (int): フレームの縦幅

        Returns:
            BlockFramework: 大本のrootとなるFrameを継承したクラスのインスタンス
        """
        cls.root: BlockFramework = BlockFramework(max_col, max_row, width, height)
        cls.root.grid_rowconfigure(0, weight=1)
        cls.root.grid_columnconfigure(0, weight=1)
        cls.root.title(title)
        return cls.root

    @classmethod
    def place_frame_widget(cls) -> None:
        """root配下のwidgetを配置する"""
        cls.root.place_frame_widget()

    @classmethod
    def create_frame(
        cls,
        frame_name: str,
        col: int = None,
        row: int = None,
        width: int = None,
        height: int = None,
        root: Any = None,
    ) -> BlockFrameBase:
        """BlockFrameとデバッグ用のキャンバスを生成する。

        Args:
            root (BlockFramework): 大本のフレーム
            frame_name (str): 生成するフレームの名称
            col (int, optional): 生成するフレームの分割行.大本のフレームの分割数と一致させる場合は指定しない. Defaults to None.
            row (int, optional): 生成するフレームの分割行.大本のフレームの分割数と一致させる場合は指定しない. Defaults to None.

        Returns:
            BlockFrame: BaseとなるFrame
        """
        if root is None:
            root: BlockFramework = cls.root
        frame: BlockFrameBase = BlockFrameBase(
            root, name=f"{root._name}-BlockFrame_{frame_name}"
        )
        # grid(row=0, column=0, sticky="nsew")だとtoplevelのとき上手くいかないのでplaceにする
        frame.place(relx=0, rely=0, relheight=1, relwidth=1)
        # BlockFrameBaseを配置する先がBlockFrameBase以外の場合は各情報がないので、rootを取得
        # Frameの場合はplace_frame_widgetが動いた後に、widthとheightが決まる。
        Inheritance_root: Any = root
        if root.__class__.__name__ != "BlockFrameBase":
            Inheritance_root = cls.root
        if col is None:
            col: int = Inheritance_root.max_col
        if row is None:
            row: int = Inheritance_root.max_row
        if width is None:
            width: int = Inheritance_root.width
        if height is None:
            height: int = Inheritance_root.height
        frame.max_col = col
        frame.max_row = row
        frame.width = width
        frame.height = height
        canvas: ResizingCanvas = ResizingCanvas(
            frame, name=f"{root._name}-canvas_{frame_name}"
        )
        canvas.layout = cls.layout(0, col, 0, row)
        return frame

    @classmethod
    def layout(
        cls,
        col_start: int,
        col_end: int,
        row_start: int,
        row_end: int,
        # 行列のセル内のオブジェクトの余白指定設定0～1
        pad_left: float = 0,
        pad_right: float = 0,
        pad_up: float = 0,
        pad_down: float = 0,
    ) -> Layout:
        """_summary_

        Args:
            col_start (int): 列の開始位置
            col_end (int): 列の終了位置
            row_start (int): 行の開始位置
            row_end (int): 行の終了位置
            pad_left (float, optional): 横幅の左側の隙間(0~1). Defaults to 0.
            pad_right (float, optional): 横幅の右側の隙間(0~1). Defaults to 0.
            pad_up (float, optional): 立幅の上側の隙間(0~1). Defaults to 0.
            pad_down (float, optional): 立幅の下側の隙間(0~1). Defaults to 0.

        Returns:
            Layout: BlockFrameworkのwidgetを配置するための位置情報
        """
        return Layout(
            col_start,
            col_end,
            row_start,
            row_end,
            pad_left=pad_left,
            pad_right=pad_right,
            pad_up=pad_up,
            pad_down=pad_down,
        )

    @classmethod
    def create_auxiliary_line(cls) -> None:
        """debug用に補助線を作成する関数

        補助線を引かない場合はこの関数をcallしないこと
        """
        cls.root.create_auxiliary_line()
