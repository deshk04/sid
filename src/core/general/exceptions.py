import logging


class SIDException(Exception):
    def __init__(self, message, object_name=None):
        # Call Exception.__init__(message)
        super().__init__(message)
        # Display the errors
        if object_name:
            self.message = 'Message: ' + str(message) + ' Object: ' + str(object_name)
        else:
            self.message = 'Message: ' + str(message)
        logging.error('Message: %s ', str(self.message))

    def __str__(self):
        return self.message
