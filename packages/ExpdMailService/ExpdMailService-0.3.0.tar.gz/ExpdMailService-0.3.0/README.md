# ExpdFtpConn

Python wrapper library for upload & download file on Expeditros Ftp Server.


How to install:

    pip install ExpdMailService


How to use with download methods:

    from ExpdMailService.send_mail import SendingMail
    SendingMail(sender="greg.he@expeditors.com", to="greg.he@expeditors.com,hegao@foxmail.com", 
                cc="greg.he@expeditors.com", subject="Test mail", attachment=[r'C:\temp\9f916dacee.html'],
                branchcode='SHA')    

