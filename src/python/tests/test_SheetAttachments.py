import smartsheetclient
import unittest
import datetime
import logging
import sys
import hashlib

log_format = '%(module)s.%(funcName)s[%(lineno)d] %(levelname)s - %(message)s'
logging.basicConfig(filename='tests.log', level=logging.DEBUG,
                    format=log_format)

api_token = 'UNSET'


class SheetAttachmentsTest(unittest.TestCase):
    def setUp(self):
        global api_token
        self.sheet_name = "UnitTestAttachments"
        self.logger = logging.getLogger()
        self.client = smartsheetclient.SmartsheetClient(api_token,
                                                        logger=self.logger)
        columns = [
            smartsheetclient.Column(
                'Item',
                type=smartsheetclient.CellTypes.TextNumber,
                primary=True),
            smartsheetclient.Column(
                'Quantity',
                type=smartsheetclient.CellTypes.TextNumber),
            smartsheetclient.Column(
                'Date',
                type=smartsheetclient.CellTypes.Date),
            smartsheetclient.Column(
                'Hash',
                type=smartsheetclient.CellTypes.TextNumber),
        ]
        self.sheet_info = self.client.createSheet(
            self.sheet_name, columns)
        self.sheet = self.sheet_info.loadSheet(attachments=True, discussions=True)
        while len(self.sheet) < 10:
            now = datetime.datetime.now()
            h = hashlib.sha256()
            h.update(str(now))
            r = self.sheet.makeRow()
            r[0] = "Padding"
            r[1] = 0
            r[2] = now.isoformat()
            r[3] = str(h.hexdigest())
            self.sheet.addRow(r)

    def tearDown(self):
        self.sheet.delete()

    def test_nop(self):
        self.assertTrue(True)

    def test_row_hyperlink_attachment(self):
        self.logger.debug("entered test_row_hyperlink_attachment")
        LINK_NAME = 'Google Search'
        LINK_URL = 'https://google.com'
        self.sheet[1].attachUrl(LINK_URL, LINK_NAME)
        sheet = self.sheet_info.loadSheet(True, True)

        path = 'sheet/{0}/row/{1}/attachments'.format(sheet.id, sheet[1].id)
        self.logger.debug("request path: {0}".format(path))
        headers, response = self.client.request(path)
        self.logger.debug(response)
        self.assertTrue(len(response) > 0)
        self.assertTrue(response[0]['attachmentType'] == u'LINK')
        self.assertTrue(response[0]['parentType'] == u'ROW')
        self.assertTrue(response[0]['name'] == LINK_NAME)
        self.assertTrue(response[0]['url'] == LINK_URL)

        self.logger.debug(dir(sheet[1].attachments[0]))
        self.logger.debug('row.hyperlink.parentType: {0}'.format(sheet[1].attachments[0].parentType))
        self.assertTrue(len(sheet[1].attachments) > 0)
        self.assertTrue(sheet[1].attachments[0].name == LINK_NAME)
        self.assertTrue(sheet[1].attachments[0].url == LINK_URL)
        self.assertTrue(sheet[1].attachments[0].attachmentType == u'LINK')
        self.assertTrue(sheet[1].attachments[0].parentType == u'ROW')
        self.logger.debug("exiting test_row_hyperlink_attachment")

    def test_row_file_attachment(self):
        self.logger.debug("entered test_row_file_attachment")
        filename = 'test_SheetAttachments.py'
        self.sheet[2].attachFile(filename)
        sheet = self.sheet_info.loadSheet(True, True)

        path = 'sheet/{0}/row/{1}/attachments'.format(self.sheet.id,
                                                      self.sheet[2].id)
        self.logger.debug("request path: {0}".format(path))
        headers, response = self.client.request(path)
        self.logger.debug(response)
        self.assertTrue(len(response) > 0)
        self.assertTrue(response[0]['attachmentType'] == u'FILE')
        self.assertTrue(response[0]['parentType'] == u'ROW')
        self.assertTrue(response[0]['name'] == filename)

        self.logger.debug(dir(sheet[2].attachments[0]))
        self.logger.debug('row.hyperlink.parentType: {0}'.format(sheet[2].attachments[0].parentType))
        self.assertTrue(len(sheet[2].attachments) > 0)
        self.assertTrue(sheet[2].attachments[0].name == filename)
        self.assertTrue(sheet[2].attachments[0].attachmentType == u'FILE')
        self.assertTrue(sheet[2].attachments[0].parentType == u'ROW')
        self.logger.debug("exiting test_row_file_attachment")

    def test_sheet_file_attachment(self):
        self.logger.debug("entered test_sheet_file_attachment")
        filename = 'test_SheetAttachments.py'
        self.sheet.attachFile(filename)
        sheet = self.sheet_info.loadSheet(True, True)
        attachments = self.sheet.attachments

        path = 'sheet/{0}/attachments'.format(self.sheet.id)
        self.logger.debug("request path: {0}".format(path))

        headers, response = self.client.request(path)
        self.logger.debug(response)
        self.assertTrue(len(response) > 0)
        self.assertTrue(response[0]['attachmentType'] == u'FILE')
        self.assertTrue(response[0]['parentType'] == u'SHEET')
        self.assertTrue(response[0]['name'] == filename)

        self.logger.debug(sheet.attachments)
        self.logger.debug('sheet.file.parentType: {0}'.format(sheet.attachments[0].parentType))
        self.assertTrue(len(sheet.attachments) > 0)
        self.assertTrue(sheet.attachments[0].name == filename)
        self.assertTrue(sheet.attachments[0].attachmentType == u'FILE')
        self.assertTrue(sheet.attachments[0].parentType == u'SHEET')
        self.logger.debug("exiting test_sheet_file_attachment")

    def test_sheet_hyperlink_attachment(self):
        self.logger.debug("entered test_sheet_hyperlink_attachment")
        LINK_NAME = 'Google Search'
        LINK_URL = 'https://google.com'
        self.sheet.attachUrl(LINK_URL, LINK_NAME)
        sheet = self.sheet_info.loadSheet(True, True)

        path = 'sheet/{0}/attachments'.format(self.sheet.id)
        self.logger.debug("request path: {0}".format(path))

        headers, response = self.client.request(path)
        self.logger.debug(response)
        self.assertTrue(len(response) > 0)
        self.assertTrue(response[0]['attachmentType'] == u'LINK')
        self.assertTrue(response[0]['parentType'] == u'SHEET')
        self.assertTrue(response[0]['name'] == LINK_NAME)
        self.assertTrue(response[0]['url'] == LINK_URL)

        self.logger.debug(sheet.attachments)
        self.logger.debug('sheet.hyperlink.parentType: {0}'.format(sheet.attachments[0].parentType))
        self.assertTrue(len(sheet.attachments) > 0)
        self.assertTrue(sheet.attachments[0].attachmentType == u'FILE')
        self.assertTrue(sheet.attachments[0].parentType == u'SHEET')
        self.assertTrue(sheet.attachments[0].name == LINK_NAME)
        self.assertTrue(sheet.attachments[0].url == LINK_URL)
        self.logger.debug("exiting test_sheet_hyperlink_attachment")


def main():
    global api_token
    if len(sys.argv) < 2:
        sys.exit("Error, must supply path to token file")
    api_token_file = sys.argv[1]

    with file(api_token_file, 'r') as fh:
        api_token = fh.read()
        api_token = api_token.strip()
    del sys.argv[1]
    unittest.main()


if __name__ == "__main__":
    main()
