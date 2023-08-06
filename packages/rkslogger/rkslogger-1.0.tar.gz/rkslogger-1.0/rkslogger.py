import logging

__version__ = '1.0'

class Logger():
    def __init__(self, name):
        self.name = name
        
        # set up logging to file - see previous section for more details
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename='app.log',
                            filemode='w')
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger().addHandler(console)
        print(type(self))
        self.logger = logging.getLogger(self.name)
        # Now, we can log to the root logger, or any other logger. First the root...

        # Now, define a couple of other loggers which might represent areas in your
        # application:
        
    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
