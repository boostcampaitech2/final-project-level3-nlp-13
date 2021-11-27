import logging

def set_logger():
    '''
        summary
            로깅 객체 및 포맷 정의
    '''
    mylogger = logging.getLogger("process")
    mylogger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    mylogger.addHandler(stream_handler)

    return mylogger
    
