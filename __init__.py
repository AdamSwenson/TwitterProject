"""
Created by adam on 6/25/18
"""
__author__ = 'adam'
import sys
import Server
import Mining
import DataAnalysis
import TextProcessingTools
import TwitterDatabase

sys.modules['Server'] = Server
sys.modules['Mining'] = Mining
sys.modules['DataAnalysis'] = DataAnalysis
sys.modules['TextProcessingTools'] = TextProcessingTools
sys.modules['TwitterDatabase'] = TwitterDatabase

