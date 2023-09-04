from django.conf import settings
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
import smtplib, ssl

def send_email(receiver_email, subject, message):
    try:
        port = 587  # For starttls
        smtp_server = settings.EMAIL_HOST
        sender_email = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD

        # Construct the email message
        email_message = f"Subject: {subject}\n\n{message}"

        # This context is used to establish a secure connection to the SMTP server.
        context = ssl.create_default_context()

        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # To initiate communication between client and SMTP server
            server.starttls(context=context) # used to upgrade the connection to a secure TLS connection
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, email_message)

        return True

    except Exception as error:
        print("Error:", error)
        return False



# @csrf_exempt

 
# def SendEmail():
#     try:
#         port = 587  # For starttls
#         smtp_server = settings.EMAIL_HOST
#         sender_email = settings.EMAIL_HOST_USER
#         receiver_email = 'palak15081@gmail.com'
#         password = settings.EMAIL_HOST_PASSWORD

#         message = f"""\


 

#         Resignation Application : Resignation Applied   """

 

#         context = ssl.create_default_context()

 
#         with smtplib.SMTP(smtp_server, port) as server:
#             server.ehlo()  # To initiate communication between client and SMTP server
#             server.starttls(context=context)
#             server.ehlo()  
#             server.login(sender_email, password)
#             server.sendmail(sender_email, receiver_email, message)

#         return True

#     except Exception as error:

#         print("Error", error)

#         return False

#         # return JsonResponse({"error": str(error)})