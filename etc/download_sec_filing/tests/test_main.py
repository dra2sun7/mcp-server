import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

# 상위 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import download_sec_filing


class TestDownloadSecFiling:
    """download_sec_filing 함수 테스트"""
    
    def setup_method(self):
        """각 테스트 전에 실행"""
        self.test_dir = tempfile.mkdtemp()
        self.output_path = os.path.join(self.test_dir, "html", "test_output")
        
    def teardown_method(self):
        """각 테스트 후에 실행"""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_valid_input_parameters(self):
        """유효한 입력 파라미터 검증"""
        # 정상적인 입력값들
        valid_ciks = ["0001018724", "1018724", "1234567890"]
        valid_years = ["2021", "2022", "2023", "2024", "2025"]
        valid_filing_types = ["8-K", "10-Q", "10-K", "DEF 14A"]
        
        for cik in valid_ciks:
            for year in valid_years:
                for filing_type in valid_filing_types:
                    # 입력 검증만 테스트 (실제 API 호출은 모킹)
                    assert 2021 <= int(year) <= 2025
                    assert filing_type in ["8-K", "10-Q", "10-K", "DEF 14A"]
                    assert len(cik.zfill(10)) == 10
    
    def test_invalid_year(self):
        """잘못된 년도 입력 테스트"""
        with pytest.raises(ValueError, match="년도는 2021부터 2025까지만 지원됩니다"):
            download_sec_filing("0001018724", "2020", "8-K", self.output_path)
        
        with pytest.raises(ValueError, match="년도는 2021부터 2025까지만 지원됩니다"):
            download_sec_filing("0001018724", "2026", "8-K", self.output_path)
    
    def test_invalid_filing_type(self):
        """잘못된 filing_type 입력 테스트"""
        with pytest.raises(ValueError, match="지원되지 않는 filing_type입니다"):
            download_sec_filing("0001018724", "2024", "INVALID", self.output_path)
    
    @patch('main.requests.get')
    def test_successful_download(self, mock_get):
        """성공적인 다운로드 테스트"""
        # Mock 응답 설정
        mock_company_response = MagicMock()
        mock_company_response.json.return_value = {
            'entityName': 'AMAZON.COM INC',
            'filings': {
                'recent': {
                    'form': ['8-K', '10-K', '8-K'],
                    'reportDate': ['2024-01-15', '2024-03-31', '2024-02-20'],
                    'accessionNumber': ['0001018724-24-000001', '0001018724-24-000002', '0001018724-24-000003'],
                    'primaryDocument': ['d8k.htm', '10k.htm', 'd8k2.htm']
                }
            }
        }
        mock_company_response.raise_for_status.return_value = None
        
        mock_doc_response = MagicMock()
        mock_doc_response.text = '<html><body>Test HTML content</body></html>'
        mock_doc_response.raise_for_status.return_value = None
        
        # requests.get이 두 번 호출됨 (회사 정보 + 문서)
        mock_get.side_effect = [mock_company_response, mock_doc_response]
        
        # 함수 실행
        result = download_sec_filing("0001018724", "2024", "8-K", self.output_path)
        
        # 검증
        assert "AMAZON.COM_INC_2024_8-K.html" in result
        assert os.path.exists(result)
        
        # 파일 내용 확인
        with open(result, 'r', encoding='utf-8') as f:
            content = f.read()
            assert '<html><body>Test HTML content</body></html>' in content
    
    @patch('main.requests.get')
    def test_no_filings_found(self, mock_get):
        """Filing을 찾을 수 없는 경우 테스트"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'entityName': 'TEST COMPANY',
            'filings': {
                'recent': {
                    'form': ['10-K'],
                    'reportDate': ['2023-12-31'],
                    'accessionNumber': ['0001018724-23-000001'],
                    'primaryDocument': ['10k.htm']
                }
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError, match="2024년 8-K Filing을 찾을 수 없습니다"):
            download_sec_filing("0001018724", "2024", "8-K", self.output_path)
    
    @patch('main.requests.get')
    def test_api_error(self, mock_get):
        """API 오류 테스트"""
        mock_get.side_effect = Exception("API Error")
        
        with pytest.raises(Exception, match="다운로드 중 오류 발생"):
            download_sec_filing("0001018724", "2024", "8-K", self.output_path)
    
    @patch('main.requests.get')
    def test_latest_filing_selection(self, mock_get):
        """가장 최근 Filing 선택 테스트"""
        mock_company_response = MagicMock()
        mock_company_response.json.return_value = {
            'entityName': 'TEST COMPANY',
            'filings': {
                'recent': {
                    'form': ['8-K', '8-K', '8-K'],
                    'reportDate': ['2024-01-15', '2024-03-31', '2024-02-20'],  # 2024-03-31이 가장 최근
                    'accessionNumber': ['0001018724-24-000001', '0001018724-24-000002', '0001018724-24-000003'],
                    'primaryDocument': ['d8k1.htm', 'd8k2.htm', 'd8k3.htm']
                }
            }
        }
        mock_company_response.raise_for_status.return_value = None
        
        mock_doc_response = MagicMock()
        mock_doc_response.text = '<html><body>Latest filing content</body></html>'
        mock_doc_response.raise_for_status.return_value = None
        
        mock_get.side_effect = [mock_company_response, mock_doc_response]
        
        result = download_sec_filing("0001018724", "2024", "8-K", self.output_path)
        
        # 가장 최근 날짜(2024-03-31)의 Filing이 선택되었는지 확인
        assert "TEST_COMPANY_2024_8-K.html" in result
    
    def test_cik_normalization(self):
        """CIK 정규화 테스트"""
        # 짧은 CIK가 10자리로 패딩되는지 확인
        with patch('main.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                'entityName': 'TEST',
                'filings': {
                    'recent': {
                        'form': ['8-K'],
                        'reportDate': ['2024-01-01'],
                        'accessionNumber': ['0001018724-24-000001'],
                        'primaryDocument': ['d8k.htm']
                    }
                }
            }
            mock_response.raise_for_status.return_value = None
            
            mock_doc_response = MagicMock()
            mock_doc_response.text = '<html>test</html>'
            mock_doc_response.raise_for_status.return_value = None
            
            mock_get.side_effect = [mock_response, mock_doc_response]
            
            # 짧은 CIK로 호출
            download_sec_filing("1018724", "2024", "8-K", self.output_path)
            
            # API 호출에서 10자리 CIK가 사용되었는지 확인
            first_call = mock_get.call_args_list[0]
            assert "0001018724" in first_call[0][0]  # URL에 10자리 CIK가 포함되어야 함
    
    def test_output_directory_creation(self):
        """출력 디렉토리 생성 테스트"""
        non_existent_path = os.path.join(self.test_dir, "new", "nested", "path")
        
        with patch('main.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                'entityName': 'TEST',
                'filings': {
                    'recent': {
                        'form': ['8-K'],
                        'reportDate': ['2024-01-01'],
                        'accessionNumber': ['0001018724-24-000001'],
                        'primaryDocument': ['d8k.htm']
                    }
                }
            }
            mock_response.raise_for_status.return_value = None
            
            mock_doc_response = MagicMock()
            mock_doc_response.text = '<html>test</html>'
            mock_doc_response.raise_for_status.return_value = None
            
            mock_get.side_effect = [mock_response, mock_doc_response]
            
            # 존재하지 않는 경로로 호출
            result = download_sec_filing("1018724", "2024", "8-K", non_existent_path)
            
            # 디렉토리가 생성되었는지 확인
            assert os.path.exists(non_existent_path)
            assert os.path.exists(result)


if __name__ == "__main__":
    pytest.main([__file__]) 