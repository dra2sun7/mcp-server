"""
커스텀 예외 클래스들
"""

class SECDownloadError(Exception):
    """SEC 다운로드 관련 에러"""
    pass


class ConversionError(Exception):
    """변환 관련 에러"""
    pass


class ConfigError(Exception):
    """설정 관련 에러"""
    pass


class FileManagerError(Exception):
    """파일 관리 관련 에러"""
    pass


class APIError(Exception):
    """API 호출 관련 에러"""
    pass 