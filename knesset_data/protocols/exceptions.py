from subprocess import CalledProcessError


class AntiwordException(CalledProcessError):

    def __str__(self):
        if not self.output:
            return "antiword processing failed, probably because antiword is not installed, try 'sudo apt-get install antiword'"
        else:
            return "antiword processing failed: {output}".format(output=self.output.split("\n")[0])


class PdftotextNotInstalledException(Exception):
    def __str__(self):
        return "pdftotext binary does not seem to be installed. Try installing it using e.g. 'sudo apt-get install poppler-utils'"


class PdftotextException(CalledProcessError):
    def __str__(self):
        if not self.output:
            return "pdftotext processing silently failed."
        else:
            return "pdftotext processing failed: {output}".format(output=self.output.split("\n")[0])
