"""Tests for ML analyzer functionality."""

import unittest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
from src.analyzers.ml_analyzer import MLAnalyzer

class TestMLAnalyzer(unittest.TestCase):
    """Test cases for MLAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test_key"
        self.analyzer = MLAnalyzer(self.api_key)
        
    def test_basic_anomaly_detection(self):
        """Test basic anomaly detection without OpenAI."""
        # Prepare test data
        metrics = {
            'rtt_samples': [10, 20, 30, 100, 20, 25],  # 100 is anomaly
            'packet_sizes': [1000, 1500, 1200, 500, 1400, 1300],  # 500 is anomaly
            'window_sizes': [8000, 8500, 8200, 4000, 8300, 8400]  # 4000 is anomaly
        }
        
        # Run detection
        anomalies = self.analyzer._basic_anomaly_detection(metrics)
        
        # Verify results
        self.assertIsInstance(anomalies, list)
        self.assertTrue(len(anomalies) > 0)
        
    def test_empty_metrics(self):
        """Test handling of empty metrics."""
        metrics = {
            'rtt_samples': [],
            'packet_sizes': [],
            'window_sizes': []
        }
        
        anomalies = self.analyzer._basic_anomaly_detection(metrics)
        self.assertEqual(anomalies, [])
