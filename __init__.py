"""
Created by adam on 6/25/18
"""
__author__ = 'adam'
import sys, os
import Server as s
import Mining as m
import DataAnalysis as da

sys.modules['Server'] = s
sys.modules['Mining'] = m
sys.modules['DataAnalysis'] = da

