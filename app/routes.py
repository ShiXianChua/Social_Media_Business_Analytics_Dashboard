"""Routes for parent Flask app."""
import PIL.Image
import pandas as pd
from flask import render_template, request, redirect, session, jsonify, abort, make_response, url_for, send_file
from flask import current_app as app
import json
import datetime
from werkzeug.utils import secure_filename
import os
import tempfile
import subprocess
import time
import urllib.parse
from PIL import Image
from app.sa.instaPostLinkScraper import InstaPostLinkScraper
from app.sa.instaCommentScraper import InstaCommentScraper
from app.sa.fbPostLinkScraper import FbPostLinkScraper
from app.sa.fbCommentScraper import FbCommentScraper
from app.ia.influencerDataScraper import InfluencerDataScraper

import pyrebase
import firebase_admin
from firebase_admin import credentials, auth, exceptions

# Flask Connect to firebase
cred = credentials.Certificate('fbAdminConfig.json')
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('fbconfig.json')))
current_user_uid = ''
current_user_email = ''


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['password']
        try:
            user = pb.auth().sign_in_with_email_and_password(email, password)
            print("login successful")
            print(user)
            print(user['localId'])
            print(type(user))
            global current_user_uid
            current_user_uid = pb.auth().get_account_info(user['idToken'])['users'][0]['localId']
            print('check')
            print(pb.auth().get_account_info(user['idToken']))
            print(current_user_uid)
            print(current_user_uid == user['localId'])
            global current_user_email
            current_user_email = email
            # Get the ID token sent by the client
            jwt = user['idToken']
            print('jwt')
            print(jwt)
            print(type(jwt))
            print('current_user_uid')
            print(current_user_uid)
            expires_in = datetime.timedelta(days=5)
            session_cookie = auth.create_session_cookie(jwt, expires_in=expires_in)
            print(session_cookie)
            print(type(session_cookie))
            myVar = b'hello'
            print(myVar)
            print(type(myVar))
            # print(type(b'ole'))
            # WHERE SETTING THE SC HAPPENS!
            session['usr'] = session_cookie
            # session['name'] = session_cookie
            print('login')
            print('sc')
            print(session_cookie)
            print(type(session_cookie))
            print('next')
            # response = jsonify({'status': 'success'})
            # Set cookie policy for session cookie.
            # expires = datetime.datetime.now() + expires_in
            # response.set_cookie(
            #     'chua_session', session_cookie, expires=expires, httponly=True, secure=True)
            # print(response.data)
            # print(response.response)
            # session['usr'] = response
            return redirect('/home')
            # return redirect(url_for('homepagess'))
            # return render_template('homepage.html')
        except exceptions.FirebaseError:
            print('ada problem')
            return abort(401, 'Failed to create a session cookie')
        except BaseException as e:
            print('login prob')
            print(e)
            print('salah')
            print(type(e))
            unsuccessful = 'Invalid credentials.'
            return render_template('login.html', umessage=unsuccessful)
    return render_template('login.html')


@app.route('/logout')
def logout():
    global current_user_uid
    global current_user_email
    current_user_uid = ''
    current_user_email = ''
    session.clear()
    # response = make_response(redirect('/login'))
    # response.set_cookie('session', expires=0)
    # return response
    return redirect('/login')


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['password']
        try:
            auth.create_user(email=email, password=password)
            successful = 'You have successfully created an account! Log in now!'
            return render_template('login.html', smessage=successful)
        except firebase_admin.auth.EmailAlreadyExistsError:
            unsuccessful = 'The email address is already linked to an existing account. Please use another one.'
            return render_template('create_account.html', umessage=unsuccessful)
        except BaseException as e:
            print(e)
            print(type(e))
            e = str(e)
            # error_json = e.args[1]
            # error = json.loads(error_json)['error']['message']
            if e == "Invalid email: \"\". Email must be a non-empty string.":
                unsuccessful = 'Invalid credentials. Make sure both email and password are filled in.'
                return render_template('create_account.html', umessage=unsuccessful)
            elif e == "Invalid password string. Password must be a string at least 6 characters long.":
                unsuccessful = 'Your password should be at least 6 characters.'
                return render_template('create_account.html', umessage=unsuccessful)
    return render_template('create_account.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        try:
            email = request.form['name']
            pb.auth().send_password_reset_email(email)
            successful = 'A password reset email has been sent to your email address.'
            return render_template('login.html', smessage=successful)
        except BaseException as e:
            print(e)
            print(type(e))
            unsuccessful = 'Failure to send password reset email. Make sure you are using the correct email address.'
            return render_template('forgot_password.html', umessage=unsuccessful)
    return render_template('forgot_password.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    try:
        # firebase_cookie = request.cookies.get('session')
        # print(firebase_cookie)
        # print(type(firebase_cookie))
        print('omess')
        print(session)
        print('holygek')
        session_cookie = session['usr']
        print(session_cookie)
        print(type(session_cookie))
        print(session['usr'])
        print(type(session['usr']))
        print(session)
        print(type(session))
        user = auth.get_user(current_user_uid)
        print('Successfully fetched user data: {0}'.format(user.uid))
    except KeyError:
        # Session cookie is unavailable. Force user to login.
        print("unavailable sc")
        return redirect('/login')
    try:
        # Verify the session cookie. In this case an additional check is added to detect
        # if the user's Firebase session was revoked, user deleted/disabled, etc.
        resp = auth.verify_session_cookie(session_cookie, check_revoked=True)
        print(resp)
        print('sudah masuk')
        email_data = {'email_address': current_user_email}
        pb.database().child(current_user_uid).child('uneditable').set(email_data)
    except auth.InvalidSessionCookieError as e:
        print(e)
        print('invalid session cookie')
        # Session cookie is invalid, expired or revoked. Force user to login.
        return redirect('/login')
    return render_template("home.html")

    # try:
    #     print('omegas')
    #     print(session['usr'])
    #     print('uhu')
    #     return render_template("homepage.html")
    # except Exception as e:
    #     print('ada errrr')
    #     print(e)
    #     print(type(e))
    #     print('ada errrror my friend')
    # return redirect('/create_account')


@app.route('/aa_guide', methods=['GET', 'POST'])
def aa_guide():
    aa_vid_file_path = pb.storage().child('tuto_videos/AudienceAnalyticsTutoVid.mp4').get_url(None)
    print(aa_vid_file_path)
    return render_template('aa_guide.html', video_path=aa_vid_file_path)


@app.route('/aa_prep', methods=['GET', 'POST'])
def aa_prep():
    return render_template('aa_prep.html')


@app.route('/psmaa_guide', methods=['GET', 'POST'])
def psmaa_guide():
    psmaa_vid_file_path = pb.storage().child('tuto_videos/PaidSocialMediaAdsAnalyticsTutoVid.mp4').get_url(None)
    print(psmaa_vid_file_path)
    return render_template('psmaa_guide.html', video_path=psmaa_vid_file_path)


@app.route('/psmaa_prep', methods=['GET', 'POST'])
def psmaa_prep():
    return render_template('psmaa_prep.html')


@app.route('/sa_guide_insta', methods=['GET', 'POST'])
def sa_guide_insta():
    sa_vid_file_path = pb.storage().child('tuto_videos/SentimentAnalysisTutoVid.mp4').get_url(None)
    print(sa_vid_file_path)
    return render_template('sa_guide_insta.html', video_path=sa_vid_file_path)


@app.route('/sa_guide_fb', methods=['GET', 'POST'])
def sa_guide_fb():
    sa_vid_file_path = pb.storage().child('tuto_videos/SentimentAnalysisTutoVid.mp4').get_url(None)
    print(sa_vid_file_path)
    return render_template('sa_guide_fb.html', video_path=sa_vid_file_path)


@app.route('/sa_scrap_insta', methods=['GET', 'POST'])
def sa_scrap_insta():
    if request.method == 'POST':
        try:
            commentList = []
            account_name = request.form['account_name']
            account_link = request.form['account_link']
            commentList.append(account_name)
            # show progress bar
            # do scraping
            postLinkScraper = InstaPostLinkScraper()
            posts, numOfPosts = postLinkScraper.scrape_post_links(account_link)
            print(posts)
            commentList.append(numOfPosts)
            commentScraper = InstaCommentScraper()
            comments = commentScraper.scrape_comments(posts)
            print(comments)
            commentList.extend(comments)
            print('show commentList')
            print(commentList)
            commentDf = pd.DataFrame(commentList)
            print(commentDf)
            # read to csv file
            full_path = os.path.realpath(__file__)
            current_dir = os.path.dirname(full_path)
            csv_filename = current_dir + r'\sa\sa_generated_datafiles' + "\\" + current_user_uid + "_sa_insta_comments.csv"
            print(csv_filename)
            commentDf.to_csv(csv_filename, index=False, header=False)
            print('to csv is success')
            # print(send_file(csv_filename, as_attachment=True))
            # print(render_template('sa_scrap_insta.html'))
            # print(redirect('/sa_prep_insta'))
            print('let user download lo')
            # allow user to download
            return send_file(csv_filename, as_attachment=True, download_name="sa_insta_comments.csv")
        except BaseException as e:
            print(e)
            print(type(e))
            print('insta web scraping ada error')
            unsuccessful1 = 'An error occurred. Please try again.'
            unsuccessful2 = 'Make sure there is an Internet connection. A browser will be opened during the process, do not close it.'
            return render_template('sa_scrap_insta.html', umessage1=unsuccessful1, umessage2=unsuccessful2)
    print(os.path.dirname(os.path.realpath(__file__)))
    print(current_user_uid)
    print(os.getcwd())
    return render_template('sa_scrap_insta.html', reminder1="Make sure there is an Internet connection.",
                           reminder2="A new browser will be opened during the process, do not close it.",
                           reminder3="Please stay on this page, the process might take a while depending on the account.")


@app.route('/sa_scrap_fb', methods=['GET', 'POST'])
def sa_scrap_fb():
    if request.method == 'POST':
        try:
            commentList = []
            page_name = request.form['page_name']
            commentList.append(page_name)
            # show progress bar
            # do scraping
            postLinkScraper = FbPostLinkScraper()
            posts, numOfPosts = postLinkScraper.scrape_post_links(page_name)
            print(posts)
            commentList.append(numOfPosts)
            commentScraper = FbCommentScraper()
            comments = commentScraper.scrape_comments(posts)
            print(comments)
            commentList.extend(comments)
            print('show commentList')
            print(commentList)
            commentDf = pd.DataFrame(commentList)
            print(commentDf)
            # read to csv file
            full_path = os.path.realpath(__file__)
            current_dir = os.path.dirname(full_path)
            csv_filename = current_dir + r'\sa\sa_generated_datafiles' + "\\" + current_user_uid + "_fb_insta_comments.csv"
            print(csv_filename)
            commentDf.to_csv(csv_filename, index=False, header=False)
            print('to csv is success')
            print(send_file(csv_filename, as_attachment=True))
            print('let user download lo')
            # allow user to download
            return send_file(csv_filename, as_attachment=True, download_name="fb_insta_comments.csv")
        except BaseException as e:
            print(e)
            print('fb web scraping ada error')
            unsuccessful1 = 'An error occurred. Please try again.'
            unsuccessful2 = 'Make sure there is an Internet connection. A browser will be opened during the process, do not close it.'
            return render_template('sa_scrap_fb.html', umessage1=unsuccessful1, umessage2=unsuccessful2)
    return render_template('sa_scrap_fb.html', reminder1="Make sure there is an Internet connection.",
                           reminder2="A new browser will be opened during the process, do not close it.",
                           reminder3="Please stay on this page, the process might take a while depending on the account.")


@app.route('/sa_prep_insta', methods=['GET', 'POST'])
def sa_prep_insta():
    return render_template('sa_prep_insta.html')


@app.route('/sa_prep_fb', methods=['GET', 'POST'])
def sa_prep_fb():
    return render_template('sa_prep_fb.html')


@app.route('/pa_guide_insta', methods=['GET', 'POST'])
def pa_guide_insta():
    pa_insta_vid_file_path = pb.storage().child('tuto_videos/PerformanceAnalyticsInstaTutoVid.mp4').get_url(None)
    print(pa_insta_vid_file_path)
    return render_template('pa_guide_insta.html', video_path=pa_insta_vid_file_path)


@app.route('/pa_guide_fb', methods=['GET', 'POST'])
def pa_guide_fb():
    pa_fb_vid_file_path = pb.storage().child('tuto_videos/PerformanceAnalyticsFbTutoVid.mp4').get_url(None)
    print(pa_fb_vid_file_path)
    return render_template('pa_guide_fb.html', video_path=pa_fb_vid_file_path)


@app.route('/pa_prep_insta', methods=['GET', 'POST'])
def pa_prep_insta():
    if request.method == 'POST':
        command = r'D:/R-4.1.2/bin/Rscript'
        arg = '--vanilla'
        # change port name 8051
        path2script = r'C:/Users/ChuaShiXian/Desktop/Bachelor of Computer Science (Information Systems)/2020-21/Semester 2 2020-21/Academic Project/Development/Eunice/Performance_Instagram/Performance_Instagram.R'
        subprocess.call([command, arg, path2script], shell=True)
        return render_template('pa_prep_insta.html')
    return render_template('pa_prep_insta.html')


@app.route('/pa_prep_fb', methods=['GET', 'POST'])
def pa_prep_fb():
    if request.method == 'POST':
        command = r'D:/R-4.1.2/bin/Rscript'
        arg = '--vanilla'
        # change port name 8052
        path2script = r'C:/Users/ChuaShiXian/Desktop/Bachelor of Computer Science (Information Systems)/2020-21/Semester 2 2020-21/Academic Project/Development/Eunice/Performance_Facebook/Performance_Facebook.R'
        subprocess.call([command, arg, path2script], shell=True)
        return render_template('pa_prep_fb.html')
    return render_template('pa_prep_fb.html')


@app.route('/ia_guide', methods=['GET', 'POST'])
def ia_guide():
    ia_vid_file_path = pb.storage().child('tuto_videos/PerformanceAnalyticsFbTutoVid.mp4').get_url(None)
    print(ia_vid_file_path)
    return render_template('ia_guide.html', video_path=ia_vid_file_path)


@app.route('/ia_scrap', methods=['GET', 'POST'])
def ia_scrap():
    if request.method == 'POST':
        # MUST ENSURE USER INSERTS AT LEAST ONE NAME
        try:
            influencer_name = request.form['influencer_name']
            print(influencer_name)
            influencer_name = influencer_name.replace(' ', '')
            print(influencer_name)
            influencer_name = influencer_name.split(',')
            print(influencer_name)
            influencer_link = ["https://www.instagram.com/pheiyong", "https://www.instagram.com/elynleonggg",
                               "https://www.instagram.com/changyonggggg", "https://www.instagram.com/wshusen",
                               "https://www.instagram.com/brysonlew", "https://www.instagram.com/syc_joycechu_",
                               "https://www.instagram.com/caventang", "https://www.instagram.com/sofyank96",
                               "https://www.instagram.com/dannyleeyuxin", "https://www.instagram.com/kevinong__"]
            for name in influencer_name:
                inf_link = "https://www.instagram.com/" + name
                influencer_link.append(inf_link)
            print(influencer_link)
            influencerDataScraper = InfluencerDataScraper()
            inf_df = influencerDataScraper.scrape_data(influencer_link)
            print(inf_df)
            print(type(inf_df))
            # # read to csv file
            full_path = os.path.realpath(__file__)
            current_dir = os.path.dirname(full_path)
            csv_filename = current_dir + r'\ia\ia_generated_datafiles' + "\\" + current_user_uid + "_ia_influencer_data.csv"
            print(csv_filename)
            inf_df.to_csv(csv_filename, index=False)
            print('to csv is success')
            # print(send_file(csv_filename, as_attachment=True))
            # print(render_template('sa_scrap_insta.html'))
            # print(redirect('/sa_prep_insta'))
            print('let user download lo')
            # allow user to download
            return send_file(csv_filename, as_attachment=True, download_name="ia_influencer_data.csv")
        except BaseException as e:
            print(e)
            print('insta web scraping ada error')
            unsuccessful1 = 'An error occurred. Please try again.'
            unsuccessful2 = 'Make sure there is an Internet connection. A browser will be opened during the process, do not close it.'
            return render_template('ia_scrap.html', umessage1=unsuccessful1, umessage2=unsuccessful2)
    return render_template('ia_scrap.html', reminder1="Make sure there is an Internet connection.",
                           reminder2="A new browser will be opened during the process, do not close it.",
                           reminder3="Please stay on this page, the process might take a while depending on the account.")


# @app.route('/ia_prep', methods=['GET', 'POST'])
# def ia_prep():
#     if request.method == 'POST':
#         command = r'D:/R-4.1.2/bin/Rscript'
#         arg = '--vanilla'
#         # change port name to 8053
#         path2script = r'C:/Users/ChuaShiXian/Desktop/Bachelor of Computer Science (Information Systems)/2020-21/Semester 2 2020-21/Academic Project/Development/Eunice/app.R'
#         subprocess.call([command, arg, path2script], shell=True)
#         return render_template('ia_prep.html')
#     return render_template('ia_prep.html')

@app.route('/ia_prep', methods=['GET', 'POST'])
def ia_prep():
    return render_template('ia_prep.html')


@app.route('/set_user_profile', methods=['GET', 'POST'])
def set_user_profile():
    if request.method == 'POST':
        try:
            pp = pb.database().child(current_user_uid).child('editable').get().val()['profile_picture']
        except BaseException as e:
            print('no pp la')
            print(e)
            pp = ''
        try:
            profile_picture = request.files['picture']
            filename = secure_filename(profile_picture.filename)
            if filename != '':
                print(filename)
                temp = tempfile.NamedTemporaryFile(delete=False)
                profile_picture.save(temp.name)
                print(temp.name)
                # convert to standard pp.png file format
                storage_path = 'users/' + current_user_uid + '/pp/pp.png'
                pb.storage().child(storage_path).put(temp.name)
                print('pp to cloud is a success!')
                pp = pb.storage().child(storage_path).get_url(None)
                print(pp)
        except BaseException as e:
            print("pp image file error")
            print(e)
        username = request.form['username']
        gender = request.form['gender']
        contact_num = request.form['contact_num']
        print(contact_num)
        print(type(contact_num))
        address = request.form['address']
        # print(address == '') True
        user_data = {'username': username, 'gender': gender, 'contact_num': contact_num, 'address': address,
                     'profile_picture': pp}
        pb.database().child(current_user_uid).child('editable').set(user_data)
        # need to change back to /user_profile
        return redirect('/user_profile')
    try:
        current_user_data = pb.database().child(current_user_uid).child('editable').get().val()
        pre_username = current_user_data['username']
        pre_contact_num = current_user_data['contact_num']
        pre_address = current_user_data['address']
        return render_template('set_user_profile.html', pre_username=pre_username, pre_contact_num=pre_contact_num,
                               pre_address=pre_address)
    except BaseException as e:
        print('setting user profile')
        print('tak de user data')
        print(e)
        print(type(e))
    return render_template('set_user_profile.html')


@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    email = pb.database().child(current_user_uid).child('uneditable').get().val()['email_address']
    try:
        current_user_data = pb.database().child(current_user_uid).child('editable').get().val()
        profile_pic = current_user_data['profile_picture']
        if profile_pic == '':
            profile_pic = "https://st4.depositphotos.com/4329009/19956/v/600/depositphotos_199564354-stock-illustration-creative-vector-illustration-default-avatar.jpg"
        username = current_user_data['username']
        gender = current_user_data['gender']
        contact_num = current_user_data['contact_num']
        address = current_user_data['address']
        return render_template('user_profile.html', email=email, profile_pic=profile_pic, username=username,
                               gender=gender, contact_num=contact_num, address=address)
    except BaseException as e:
        print('user profile')
        print('tak de user data')
        print(e)
        print(type(e))
        profile_pic = "https://st4.depositphotos.com/4329009/19956/v/600/depositphotos_199564354-stock-illustration-creative-vector-illustration-default-avatar.jpg"
    print('huho')
    return render_template('user_profile.html', email=email, profile_pic=profile_pic)

# @app.route('/aa_prep', methods=['GET', 'POST'])
# def aa_prep():
#     if request.method == 'POST':
#         uploaded_file = request.files['file']
#         filename = secure_filename(uploaded_file.filename)
#         print(filename)
#         if filename != '':
#             file_ext = os.path.splitext(filename)[1]
#             print(file_ext)
#             if file_ext not in app.config['UPLOAD_EXTENSIONS']:
#                 print('file ext error')
#                 return render_template('aa_prep.html', smessage="Invalid file extension")
#             temp = tempfile.NamedTemporaryFile(delete=False)
#             print(temp)
#             uploaded_file.save(temp.name)
#             print(temp.name)
#             storage_path = current_user_uid + '/AA/' + filename
#             pb.storage().child(storage_path).put(temp.name)
#             cloud_file_path = pb.storage().child(storage_path).get_url(None)
#             print(cloud_file_path)
#             session['aa_file_path'] = cloud_file_path
#             print('url_for')
#             query = cloud_file_path
#             print(urllib.parse.quote(query, safe=''))
#             encoded_cloud_file_path = urllib.parse.quote(query, safe='')
#             # print(url_for('aa_execute', name=cloud_file_path))
#             return redirect(url_for('aa_execute', fpath=encoded_cloud_file_path))
#             # file_db_date = {'name':filename, 'filepath':filepath}
#             # pb.database().child()
#             # Clean-up temp image
#             # os.remove(temp.name)
#     return render_template('aa_prep.html')

# @app.route("/aa_execute/<fpath>")
# def aa_execute(fpath):
#     print('ohyes')
#     print(fpath)
#     print('ohyeah')
#     return render_template('aa_execute.html')

# @app.route('/aa_prep_select', methods=['GET', 'POST'])
# def aa_prep_select():
# if request.method == 'POST':
# storage_path = current_user_uid + '/AA/'
# allFiles = pb.storage().child(storage_path).get()
# allFiles = pb.storage().list_files()
# print(allFiles)
# return render_template('aa_prep_select.html')
