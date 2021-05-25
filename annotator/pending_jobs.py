#----------------------------------------------
# @author: Kowndinya Boyalakuntla <cs17b032@iittp.ac.in>
# @date: 22/01/2021
#----------------------------------------------
from pymongo import MongoClient
from xml.dom import minidom
import sys
import os
def generate_template(user_email,path):
    ''' Generates user annotations job template based on information present in the database '''
    try:
        connection = MongoClient('localhost',27017)
        print("connected Succesfully!!!")
        db = connection.get_database('anno_admin')
        collections = db.list_collection_names()
        print(collections)
        if("author_job" in collections):
            query = {"email" : user_email}
            document = db["author_job"].find(query)[0]
            jobs =  document["jobs"]
            pending_jobs = []
            completed_jobs = []
            status_list = jobs.split(",")
            complete = 0
            for job_status in status_list:
                job = job_status.split(":")
                if(job[1] == 'pending'):
                    pending_jobs.append(job[0])
                elif(job[1] == 'complete'):
                    completed_jobs.append(job[0])
            pending = len(pending_jobs)
            complete = len(completed_jobs)
            assigned = complete + pending
            fp = open(path, 'w')
            fp.write('')
            fp.close()
            fp = open(path, 'a')
            fp.write(
            '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Profile Annotator</title>
  <meta content="width=device-width, initial-scale=1.0" name="viewport">
  <meta content="" name="keywords">
  <meta content="" name="description">


  <link rel="apple-touch-icon" sizes="180x180" href="https://kowndinya2000.github.io/header-logo.github.io/apple-touch-icon.png">
  <link rel="icon" type="image/png" sizes="32x32" href="https://kowndinya2000.github.io/header-logo.github.io/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="https://kowndinya2000.github.io/header-logo.github.io/favicon-16x16.png">
  <link rel="manifest" href="https://kowndinya2000.github.io/header-logo.github.io/site.webmanifest">

  <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,500,600,700,700i|Montserrat:300,400,500,600,700" rel="stylesheet">

  <link href="https://annotator-web-resources.github.io/tool-resources.github.io/profile_lib/bootstrap/css/bootstrap.min.css" rel="stylesheet">

  <link href="https://annotator-web-resources.github.io/tool-resources.github.io/profile_lib/font-awesome/css/font-awesome.min.css" rel="stylesheet">
  <link href="https://annotator-web-resources.github.io/tool-resources.github.io/profile_lib/animate/animate.min.css" rel="stylesheet">
  <link href="https://annotator-web-resources.github.io/tool-resources.github.io/profile_lib/ionicons/css/ionicons.min.css" rel="stylesheet">
  <link href="https://annotator-web-resources.github.io/tool-resources.github.io/profile_lib/owlcarousel/assets/owl.carousel.min.css" rel="stylesheet">
  <link href="https://annotator-web-resources.github.io/tool-resources.github.io/profile_lib/lightbox/css/lightbox.min.css" rel="stylesheet">

  <link href="https://annotator-web-resources.github.io/tool-resources.github.io/profile.css" rel="stylesheet">
  <style>
::-webkit-scrollbar {
                    width: 12px;
                }
::-webkit-scrollbar-track {
                background: transparent;
                }

::-webkit-scrollbar-thumb {
                background-color: #434190;
                background-color: #333;
                border-radius: 20px;
                border: 3px solid white;
                }

  </style>
  <style>

      .btn-done {
                      background-color: black;
                      border: 0;
                      border-radius: 8px;
                      box-shadow: 0 10px 10px rgba(0, 0, 0, 0.2);
                      color: #fff;
                      font-size: 12px;
                      padding: 12px 12px;

                  }
                  .btn-pend {
                      background-color: crimson;
                      border: 0;
                      border-radius: 8px;
                      box-shadow: 0 10px 10px rgba(0, 0, 0, 0.2);
                      color: #fff;
                      font-size: 12px;
                      padding: 12px 12px;

                  }
  </style>
</head>

<body>

  <main id="main">
<section id="services" class="section-bg">
<div class="container">
<header class="section-header" style="">
  <link rel='stylesheet' href='https://use.fontawesome.com/releases/v5.0.13/css/all.css'>
  <link rel="stylesheet" href="https://annotator-web-resources.github.io/tool-resources.github.io/tab_style.css">
  <div class="wrapper">
    <h2 style="text-transform: uppercase;">Your profile</h2>
    <h6></h6>
    <nav class="tabs">
      <div class="selector"></div>
      <a href="#telugu" class="active" onclick="tel()"><span style="color: #0D2D63;margin-right: 1rem;font-weight: 900;">అ</span>Telugu</a>
      <a href="#devanagari" onclick="dev()"><span style="color: #0D2D63;margin-right: 1rem;font-weight: 900;">ऋ</span>Devanagari</a>
      <a href="#kannada" onclick="kann()"><span style="color: #0D2D63;margin-right: 1rem;font-weight: 900;">ಕ</span>Kannada</a>
      <a href="#health" onclick="heal()"><span style="color: #0D2D63;margin-right: 1rem;font-weight: 900;">H</span>Health Scripts</a>
      <a href="#english" onclick="en()"><span style="color: #0D2D63;margin-right: 1rem;font-weight: 900;">Y</span>English</a>
      <a href="#mixed" onclick="mix()"><span style="color: #0D2D63;margin-right: 1rem;font-weight: 900;">HఅY</span>Mixed</a>
    </nav>
  </div>
  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js'></script><script  src="https://annotator-web-resources.github.io/tool-resources.github.io/tab_script.js"></script>
  <a href="#telugu" id="a1" style="display: none;">telugu</a>
  <a href="#devanagari" id="a2" style="display: none;">devanagari</a>
  <a href="#kannada" id="a3" style="display: none;">kannada</a>
  <a href="#health" id="a4" style="display: none;">health scripts</a>
  <a href="#english" id="a5" style="display: none;">english</a>
  <a href="#mixed" id="a6" style="display: none;">mixed</a>
  <script>
    function kann(){
      document.getElementById('a3').click()
    }
    function tel(){
      document.getElementById('a1').click()
    }
    function dev(){
      document.getElementById('a2').click()
    }
    function en(){
      document.getElementById('a5').click()
    }
    function heal(){
      document.getElementById('a4').click()
    }
    function mix(){
      document.getElementById('a6').click()
    }
  </script>
</header>
<p style="max-height: 30rem;overflow-y: scroll;">
<div class="row" id="telugu" style="">
  <iframe src="https://annotator-web-resources.github.io/tool-resources.github.io/fade-in-text/telugu.html" style="width: 100%; height: 15rem;right: 0;border: none;position: absolute;"></iframe>
  <div class="col-md-6 col-lg-4 wow bounceInUp" data-wow-duration="1.4s" style="margin-top: 12rem;">
                <img src="/Images/profile-images/document1.jpg" alt="USER DOCUMENTS FOR ANNOTATION" style="width: 100%;background-size: cover;">
                <div class="box" >
                  <h4 class="title"><a href="#">document1</a></h4>
                  <p class="description" style="color: #333;font-weight: bold;text-align: center;">DOCUMENT LANGUAGE: <span style="color: #4457C0;">TELUGU</span></p>
                  <br>
            '''
            )
            fp.close()
            fp = open(path,'a')
            pend_list = []
            for pend in pending_jobs:
                pend_list.append(pend)
            fp.write('''
                        <div style="flex: 1">
                        <div style="display: flex;flex-direction: row;">
                        <div style="flex: 1;margin-bottom: 1rem;">
                        <button class="btn-pend">
                            {% if current_user.is_authenticated %}''' +
                            '''<a href="/annotate?collection=LabelMe'''
                            +user_email
                            +'''&mode=i&folder=docs_'''
                            +user_email
                            +'''&image='''
                            +"document1.jpg"
                            +'''&username='''
                            +user_email
                            +'"'+'''
                            style="text-decoration: none;color: white;font-weight: bold;"> '''+
                        '''
                        ANNOTATE
                        </a>
                        {% endif %}
                        </button>
                        </div>
                        <div style="flex: 1">
                            <button class="btn-done" style="font-weight: bold;">
                              {% if current_user.is_authenticated %}''' +
                              '''<a href="/complete?image='''
                              +"document1.jpg"
                              +'''&username='''
                              +user_email
                              +'"'+'style="text-decoration: none;color: white;font-weight: bold;">' +
                               '''
                                I AM DONE
                            </a>
                              {% endif %}
                            </button>
                        </div>
                        </div>
                        </div>
                        </div>
                        </div>
                     ''')
            # fp.close()
            fp.write('''
                        
                                            </div>
                    ''')
            # fp.close()
            fp.write('''
                        <div class="row" id="devanagari">
                        <iframe src="https://annotator-web-resources.github.io/tool-resources.github.io/fade-in-text/devanagari.html" style="width: 100%; height: 15rem;right: 0;border: none;position: absolute;"></iframe>
                        <div class="col-md-6 col-lg-4 wow bounceInUp" data-wow-duration="1.4s" style="margin-top: 12rem;">
                        <img src="/Images/profile-images/document2.jpg" alt="USER DOCUMENTS FOR ANNOTATION" style="width: 100%;">
                        <div class="box">
                            <h4 class="title"><a href="#">document2</a></h4>
                            <p class="description" style="color: #333;font-weight: bold;text-align: center;">DOCUMENT LANGUAGE: <span style="color: #4457C0;">DEVANAGARI</span></p>
                            <br>
                            <div style="flex: 1">
                            <div style="display: flex;flex-direction: row;">
                                <div style="flex: 1;margin-bottom: 1rem;">
                                    <button class="btn-pend">
                                    {% if current_user.is_authenticated %}''' +
                                                  '''<a href="/annotate?collection=LabelMe'''
                                                  +user_email
                                                  +'''&mode=i&folder=docs_'''
                                                  +user_email
                                                  +'''&image='''
                                                  +"document2.jpg"
                                                  +'''&username='''
                                                  +user_email
                                                  +'"'+'''
                                                  style="text-decoration: none;color: white;font-weight: bold;"> '''+
                                              '''
                                              ANNOTATE
                                              </a>
                                              {% endif %}
                                    </button>
                                    </div>
                                    <div style="flex: 1">
                                    <button class="btn-done" style="font-weight: bold;">
                                        {% if current_user.is_authenticated %}''' +
                                                       '''<a href="/complete?image='''
                                                       +"document2.jpg"
                                                       +'''&username='''
                                                       +user_email
                                                       +'"'+'style="text-decoration: none;color: white;font-weight: bold;">' +
                                                        '''
                                                         I AM DONE
                                                     </a>
                                                       {% endif %}
                                                     </button>
                                        </div>
                                        </div>
                                        </div>
                                        </div>
                                        </div>
                                        </div>

                    ''')
            # fp.close()
            fp.write('''
                        <div class="row" id="kannada">
                        <iframe src="https://annotator-web-resources.github.io/tool-resources.github.io/fade-in-text/kannada.html" style="width: 100%; height: 15rem;right: 0;border: none;position: absolute;"></iframe>
                        <div class="col-md-6 col-lg-4 wow bounceInUp" data-wow-duration="1.4s" style="margin-top: 12rem;">
                        <img src="/Images/profile-images/document3.jpg" alt="USER DOCUMENTS FOR ANNOTATION" style="width: 100%;">
                        <div class="box">
                        <h4 class="title"><a href="#">document3</a></h4>
                        <p class="description" style="color: #333;font-weight: bold;text-align: center;">DOCUMENT LANGUAGE: <span style="color: #4457C0;">KANNADA</span></p>
                        <br>
                        <div style="flex: 1">
                        <div style="display: flex;flex-direction: row;">
                            <div style="flex: 1;margin-bottom: 1rem;">
                                <button class="btn-pend">
                                {% if current_user.is_authenticated %}''' +
                                              '''<a href="/annotate?collection=LabelMe'''
                                              +user_email
                                              +'''&mode=i&folder=docs_'''
                                              +user_email
                                              +'''&image='''
                                              +"document3.jpg"
                                              +'''&username='''
                                              +user_email
                                              +'"'+'''
                                              style="text-decoration: none;color: white;font-weight: bold;"> '''+
                                          '''
                                          ANNOTATE
                                          </a>
                                          {% endif %}
                                </button>
                                </div>
                                <div style="flex: 1">
                                <button class="btn-done" style="font-weight: bold;">
                                {% if current_user.is_authenticated %}''' +
                                               '''<a href="/complete?image='''
                                               +"document3.jpg"
                                               +'''&username='''
                                               +user_email
                                               +'"'+'style="text-decoration: none;color: white;font-weight: bold;">' +
                                                '''
                                                 I AM DONE
                                             </a>
                                               {% endif %}
                                             </button>
                                </div>
                                </div>
                                </div>
                                </div>
                                </div>
                                </div>
                    ''')
            # fp.close()
            fp.write('''
                        <div class="row" id="health">
                        <iframe src="https://annotator-web-resources.github.io/tool-resources.github.io/fade-in-text/health_scripts.html" style="width: 100%; height: 15rem;right: 0;border: none;position: absolute;"></iframe>
                        <div class="col-md-6 col-lg-4 wow bounceInUp" data-wow-duration="1.4s" style="margin-top: 12rem;">
                        <img src="/Images/profile-images/document4.jpg" alt="USER DOCUMENTS FOR ANNOTATION" style="width: 100%;background-size: cover;">
                        <div class="box" >
                        <h4 class="title"><a href="#">document4</a></h4>
                        <p class="description" style="color: #333;font-weight: bold;text-align: center;">DOCUMENT TYPE: <span style="color: #4457C0;">HEALTH SCRIPT</span></p>
                        <br>
                        <div style="flex: 1">
                        <div style="display: flex;flex-direction: row;">
                            <div style="flex: 1;margin-bottom: 1rem;">
                                <button class="btn-pend">
                                {% if current_user.is_authenticated %}''' +
                                            '''<a href="/annotate?collection=LabelMe'''
                                            +user_email
                                            +'''&mode=i&folder=docs_'''
                                            +user_email
                                            +'''&image='''
                                            +"document4.jpg"
                                            +'''&username='''
                                            +user_email
                                            +'"'+'''
                                            style="text-decoration: none;color: white;font-weight: bold;"> '''+
                                            '''
                                            ANNOTATE
                                            </a>
                                            {% endif %}
                                            </button>
                                            </div>
                                            <div style="flex: 1">
                                            <button class="btn-done" style="font-weight: bold;">
                                            {% if current_user.is_authenticated %}''' +
                                            '''<a href="/complete?image='''
                                            +"document4.jpg"
                                            +'''&username='''
                                            +user_email
                                            +'"'+'style="text-decoration: none;color: white;font-weight: bold;">' +
                                                '''
                                                I AM DONE
                                                </a>
                                                {% endif %}
                                                </button>
                                                </div>
                                                </div>
                                                </div>
                                                </div>
                                                </div>
                                                </div>

                    ''')
            # fp.close()
            fp.write('''
                        <div class="row" id="english">
                        <iframe src="https://annotator-web-resources.github.io/tool-resources.github.io/fade-in-text/english.html" style="width: 100%; height: 15rem;right: 0;border: none;position: absolute;"></iframe>
                        <div class="col-md-6 col-lg-4 wow bounceInUp" data-wow-duration="1.4s" style="margin-top: 12rem;">
                        <img src="/Images/profile-images/document5.jpg" alt="USER DOCUMENTS FOR ANNOTATION" style="width: 100%;background-size: cover;">
                        <div class="box" >
                        <h4 class="title"><a href="#">document5</a></h4>
                        <p class="description" style="color: #333;font-weight: bold;text-align: center;">DOCUMENT LANGUAGE: <span style="color: #4457C0;">ENGLISH</span></p>
                        <br>
                        <div style="flex: 1">
                        <div style="display: flex;flex-direction: row;">
                            <div style="flex: 1;margin-bottom: 1rem;">
                                <button class="btn-pend">
                                {% if current_user.is_authenticated %}''' +
                                            '''<a href="/annotate?collection=LabelMe'''
                                            +user_email
                                            +'''&mode=i&folder=docs_'''
                                            +user_email
                                            +'''&image='''
                                            +"document5.jpg"
                                            +'''&username='''
                                            +user_email
                                            +'"'+'''
                                            style="text-decoration: none;color: white;font-weight: bold;"> '''+
                                            '''
                                            ANNOTATE
                                            </a>
                                            {% endif %}
                                            </button>
                                            </div>
                                            <div style="flex: 1">
                                            <button class="btn-done" style="font-weight: bold;">
                                            {% if current_user.is_authenticated %}''' +
                                                '''<a href="/complete?image='''
                                                +"document5.jpg"
                                                +'''&username='''
                                                +user_email
                                                +'"'+'style="text-decoration: none;color: white;font-weight: bold;">' +
                                                '''
                                                I AM DONE
                                                </a>
                                                {% endif %}
                                                </button>
                                                </div>
                                                </div>
                                                </div>
                                                </div>
                                                </div>
                                                <div class="col-md-6 col-lg-4 wow bounceInUp" data-wow-duration="1.4s" style="margin-top: 12rem;">
                                                <img src="/Images/profile-images/document6.jpg" alt="USER DOCUMENTS FOR ANNOTATION" style="width: 100%;background-size: cover;">
                                                <div class="box" >
                                                <h4 class="title"><a href="#">document6</a></h4>
                                                <p class="description" style="color: #333;font-weight: bold;text-align: center;">DOCUMENT LANGUAGE: <span style="color: #4457C0;">ENGLISH</span></p>
                                                <br>
                                                <div style="flex: 1">
                                                <div style="display: flex;flex-direction: row;">
                                                <div style="flex: 1;margin-bottom: 1rem;">
                                                <button class="btn-pend">
                                                {% if current_user.is_authenticated %}''' +
                                                '''<a href="/annotate?collection=LabelMe'''
                                                +user_email
                                                +'''&mode=i&folder=docs_'''
                                                +user_email
                                                +'''&image='''
                                                +"document6.jpg"
                                                +'''&username='''
                                                +user_email
                                                +'"'+'''
                                                style="text-decoration: none;color: white;font-weight: bold;"> '''+
                                                '''
                                                ANNOTATE
                                                </a>
                                                {% endif %}
                                                </button>
                                                </div>
                                                <div style="flex: 1">
                                                <button class="btn-done" style="font-weight: bold;">
                                                {% if current_user.is_authenticated %}''' +
                                                '''<a href="/complete?image='''
                                                +"document6.jpg"
                                                +'''&username='''
                                                +user_email
                                                +'"'+'style="text-decoration: none;color: white;font-weight: bold;">' +
                                                '''
                                                I AM DONE
                                                </a>
                                                {% endif %}
                                                </button>
                                                </div>
                                                </div>
                                                </div>
                                                </div>
                                                </div>
                                                </div>

                    ''')
            # fp.close()
            fp.write('''
                        <div class="row" id="mixed">
                                    <iframe src="https://annotator-web-resources.github.io/tool-resources.github.io/fade-in-text/mixed.html" style="width: 100%; height: 15rem;right: 0;border: none;position: absolute;"></iframe>
                                    <div class="col-md-6 col-lg-4 wow bounceInUp" data-wow-duration="1.4s" style="margin-top: 12rem;">
                                    <img src="/Images/profile-images/document7.jpg" alt="USER DOCUMENTS FOR ANNOTATION" style="width: 100%;background-size: cover;">
                                    <div class="box" >
                                    <h4 class="title"><a href="#">document7</a></h4>
                                    <p class="description" style="color: #333;font-weight: bold;text-align: center;">DOCUMENT LANGUAGE: <span style="color: #4457C0;">MIXED</span></p>
                                    <br>
                                    <div style="flex: 1">
                                    <div style="display: flex;flex-direction: row;">
                                        <div style="flex: 1;margin-bottom: 1rem;">
                                            <button class="btn-pend">
                                            {% if current_user.is_authenticated %}''' +
                                                        '''<a href="/annotate?collection=LabelMe'''
                                                        +user_email
                                                        +'''&mode=i&folder=docs_'''
                                                        +user_email
                                                        +'''&image='''
                                                        +"document7.jpg"
                                                        +'''&username='''
                                                        +user_email
                                                        +'"'+'''
                                                        style="text-decoration: none;color: white;font-weight: bold;"> '''+
                                                        '''
                                                        ANNOTATE
                                                        </a>
                                                        {% endif %}
                                                        </button>
                                                        </div>
                                                        <div style="flex: 1">
                                                        <button class="btn-done" style="font-weight: bold;">
                                                        {% if current_user.is_authenticated %}''' +
                                                            '''<a href="/complete?image='''
                                                            +"document7.jpg"
                                                            +'''&username='''
                                                            +user_email
                                                            +'"'+'style="text-decoration: none;color: white;font-weight: bold;">' +
                                                            '''
                                                            I AM DONE
                                                            </a>
                                                            {% endif %}
                                                            </button>
                                                            </div>
                                                            </div>
                                                            </div>
                                                            </div>
                                                            </div>
                                                            <div class="col-md-6 col-lg-4 wow bounceInUp" data-wow-duration="1.4s" style="margin-top: 12rem;">
                                    <img src="/Images/profile-images/document8.jpg" alt="USER DOCUMENTS FOR ANNOTATION" style="width: 100%;background-size: cover;">
                                    <div class="box" >
                                    <h4 class="title"><a href="#">document8</a></h4>
                                    <p class="description" style="color: #333;font-weight: bold;text-align: center;">DOCUMENT LANGUAGE: <span style="color: #4457C0;">MIXED</span></p>
                                    <br>
                                    <div style="flex: 1">
                                    <div style="display: flex;flex-direction: row;">
                                        <div style="flex: 1;margin-bottom: 1rem;">
                                            <button class="btn-pend">
                                            {% if current_user.is_authenticated %}''' +
                                                        '''<a href="/annotate?collection=LabelMe'''
                                                        +user_email
                                                        +'''&mode=i&folder=docs_'''
                                                        +user_email
                                                        +'''&image='''
                                                        +"document8.jpg"
                                                        +'''&username='''
                                                        +user_email
                                                        +'"'+'''
                                                        style="text-decoration: none;color: white;font-weight: bold;"> '''+
                                                        '''
                                                        ANNOTATE
                                                        </a>
                                                        {% endif %}
                                                        </button>
                                                        </div>
                                                        <div style="flex: 1">
                                                        <button class="btn-done" style="font-weight: bold;">
                                                        {% if current_user.is_authenticated %}''' +
                                                            '''<a href="/complete?image='''
                                                            +"document8.jpg"
                                                            +'''&username='''
                                                            +user_email
                                                            +'"'+'style="text-decoration: none;color: white;font-weight: bold;">' +
                                                            '''
                                                            I AM DONE
                                                            </a>
                                                            {% endif %}
                                                            </button>
                                                            </div>
                                                            </div>
                                                            </div>
                                                            </div>
                                                            </div>
                                    
                                                            <div class="col-md-6 col-lg-4 wow bounceInUp" data-wow-duration="1.4s" style="margin-top: 12rem;">
                                                            <img src="/Images/profile-images/document9.jpg" alt="USER DOCUMENTS FOR ANNOTATION" style="width: 100%;background-size: cover;">
                                                            <div class="box" >
                                                            <h4 class="title"><a href="#">document9</a></h4>
                                                            <p class="description" style="color: #333;font-weight: bold;text-align: center;">DOCUMENT LANGUAGE: <span style="color: #4457C0;">MIXED</span></p>
                                                            <br>
                                                            <div style="flex: 1">
                                                            <div style="display: flex;flex-direction: row;">
                                                                <div style="flex: 1;margin-bottom: 1rem;">
                                                                    <button class="btn-pend">
                                                                    {% if current_user.is_authenticated %}''' +
                                                                                '''<a href="/annotate?collection=LabelMe'''
                                                                                +user_email
                                                                                +'''&mode=i&folder=docs_'''
                                                                                +user_email
                                                                                +'''&image='''
                                                                                +"document9.jpg"
                                                                                +'''&username='''
                                                                                +user_email
                                                                                +'"'+'''
                                                                                style="text-decoration: none;color: white;font-weight: bold;"> '''+
                                                                                '''
                                                                                ANNOTATE
                                                                                </a>
                                                                                {% endif %}
                                                                                </button>
                                                                                </div>
                                                                                <div style="flex: 1">
                                                                                <button class="btn-done" style="font-weight: bold;">
                                                                                {% if current_user.is_authenticated %}''' +
                                                                                    '''<a href="/complete?image='''
                                                                                    +"document9.jpg"
                                                                                    +'''&username='''
                                                                                    +user_email
                                                                                    +'"'+'style="text-decoration: none;color: white;font-weight: bold;">' +
                                                                                    '''
                                                                                    I AM DONE
                                                                                    </a>
                                                                                    {% endif %}
                                                                                    </button>
                                                                                    </div>
                                                                                    </div>
                                                                                    </div>
                                                                                    </div>
                                                                                    </div>
                        </div>
                                                </p>


                                                </div>
                                                </section>



                                                </main>


                                                <a href="#" class="back-to-top" style="background:#343A40"><i class="fa fa-chevron-up"></i></a>
                                                <script src="https://annotator-web-resources.github.io/tool-resources.github.io/profile_lib/jquery/jquery.min.js"></script>
                                                <script src="https://annotator-web-resources.github.io/tool-resources.github.io/profile_lib/jquery/jquery-migrate.min.js"></script>
                                                <script src="https://annotator-web-resources.github.io/tool-resources.github.io/profile_lib/bootstrap/js/bootstrap.bundle.min.js"></script>
                                                <script src="https://annotator-web-resources.github.io/tool-resources.github.io/profile_lib/easing/easing.min.js"></script>
                                                <script src="https://annotator-web-resources.github.io/tool-resources.github.io/profile_lib/mobile-nav/mobile-nav.js"></script>
                                                <script src="https://annotator-web-resources.github.io/tool-resources.github.io/profile_lib/wow/wow.min.js"></script>
                                                <script src="https://annotator-web-resources.github.io/tool-resources.github.io/profile_lib/waypoints/waypoints.min.js"></script>
                                                <script src="https://annotator-web-resources.github.io/tool-resources.github.io/profile_lib/counterup/counterup.min.js"></script>
                                                <script src="https://annotator-web-resources.github.io/tool-resources.github.io/profile_lib/owlcarousel/owl.carousel.min.js"></script>
                                                <script src="https://annotator-web-resources.github.io/tool-resources.github.io/profile_lib/isotope/isotope.pkgd.min.js"></script>
                                                <script src="https://annotator-web-resources.github.io/tool-resources.github.io/profile_lib/lightbox/js/lightbox.min.js"></script>
                                                <script src="https://annotator-web-resources.github.io/tool-resources.github.io/profile_js/main.js"></script>

                                                </body>
                                                </html>

                    ''')
            fp.close()

            return True
        else:
            print("No collection author_job as such!!")
            return False
    except Exception as e:
        print(e)
        return False
  