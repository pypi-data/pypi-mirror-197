#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""BlockFrameBase"""
from typing import Any
from tkinter import ttk


class BlockFrameBase(ttk.Frame):
    """BlockFrameworkで操作するための土台となるクラス"""

    def __init__(self, root: Any, **kwargs) -> None:
        """コンストラクタ

        Args:
            root (Any): このフレームを配置する先の親フレーム
        """
        super().__init__(root, **kwargs)
