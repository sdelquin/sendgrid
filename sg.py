import sendgrid
import base64
import os


class SendGrid:

    def __init__(self, apikey, from_addr, from_name):
        self.sg = sendgrid.SendGridAPIClient(apikey=apikey)
        self.data = {
            "personalizations": [{
                "to": [],
                "subject": None
            }],
            "from": {
                "email": from_addr,
                "name": from_name
            },
            "content": [{
                "type": "text/plain",
                "value": None
            }]
        }

    def send(self, to, subject, msg, cc=[], bcc=[], attachments=[]):
        # personalizations -> to
        addrs = to if type(to) == list else [to]
        for addr in addrs:
            self.data["personalizations"][0]["to"].append({"email": addr})
        # personalizations -> subject
        self.data["personalizations"][0]["subject"] = subject
        # content -> value
        self.data["content"][0]["value"] = msg
        # personalizations -> cc
        if cc:
            self.data["personalizations"][0]["cc"] = []
            addrs = cc if type(cc) in (list, tuple) else [cc]
            for addr in addrs:
                self.data["personalizations"][0]["cc"].append({"email": addr})
        # personalizations -> bcc
        if bcc:
            self.data["personalizations"][0]["bcc"] = []
            addrs = bcc if type(bcc) in (list, tuple) else [bcc]
            for addr in addrs:
                self.data["personalizations"][0]["bcc"].append({"email": addr})

        if attachments:
            self.data["attachments"] = []
            attachments = attachments if type(attachments) in (list, tuple) \
                else [attachments]
            for attachment in attachments:
                with open(attachment, "rb") as f:
                    file_content = f.read()
                    f.close()
                encoded_file_content = base64.b64encode(file_content).decode()
                self.data["attachments"].append({
                    "content": encoded_file_content,
                    "filename": os.path.split(attachment)[1]
                })

        self.response = self.sg.client.mail.send.post(request_body=self.data)

        # print(self.response.status_code)
        # print(self.response.body)
        # print(self.response.headers)
