"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai
import data_to_prompt as dtp
import prompt_to_data as ptd

genai.configure(api_key="AIzaSyDZsL9E5neuBkRNlm1574SK3divZgoEEMw")

defaults = {
  'model': 'models/text-bison-001',
  'temperature': 0.2,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
  'max_output_tokens': 100000,
  'stop_sequences': [],
  'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":4},{"category":"HARM_CATEGORY_TOXICITY","threshold":4},{"category":"HARM_CATEGORY_VIOLENCE","threshold":4},{"category":"HARM_CATEGORY_SEXUAL","threshold":4},{"category":"HARM_CATEGORY_MEDICAL","threshold":4},{"category":"HARM_CATEGORY_DANGEROUS","threshold":4}],
}


def prompt(input):
  return f"""I  gave you a number of titles of running processes of a computer.
  You will only tell whether the running process is directly productive that is good for his career, for a specific profession of a person.
  Each line in the input will be treated as each process title.
  You will give answer in true or false.
  input: Profession :- College student studying computer science

  1.C:\WINDOWS\py.exe
  2.SAI AND SE 5th sem
  3.test_removebrackets.py,SAI AND SE 5th sem,Visual Studio Code
  4.A new approach to container and wrapper classes,YouTube,Opera
  5.2023-11-14.csv,SAI AND SE 5th sem,Visual Studio Code
  6.WPS Office
  7.dsp6nov.docx,WPS Office
  8.dsp6nov.docx Property
  9.Downloads
  10.dsp6nov Properties



  output: 1.C:\WINDOWS\py.exe : true
  2.SAI AND SE 5th sem : true
  3.test_removebrackets.py,SAI AND SE 5th sem,Visual Studio Code : true
  4.A new approach to container and wrapper classes,YouTube,Opera : true
  5.2023-11-14.csv,SAI AND SE 5th sem,Visual Studio Code : true
  6.WPS Office : false
  7.dsp6nov.docx,WPS Office : true
  8.dsp6nov.docx Property : true
  9.Downloads : false
  10.dsp6nov Properties : false


  input: Profession :- College student studying computer science

  Processes:
  1.difference between cookies and cache,Google Search,Opera
  2.Daily Activity Tracking,Personal,Microsoft​ Edge
  3.Save
  4.styles.css,googlechat,Visual Studio Code
  5.index.html,googlechat,Visual Studio Code
  6.Google Chat and 1 more page,Personal,Microsoft​ Edge
  7.DevTools
  8.DevTools,127.0.0.1:3000/index.html
  output: 1.difference between cookies and cache,Google Search,Opera : true
  2.Daily Activity Tracking,Personal,Microsoft​ Edge : false
  3.Save : false
  4.styles.css,googlechat,Visual Studio Code : true
  5.index.html,googlechat,Visual Studio Code : true
  6.Google Chat and 1 more page,Personal,Microsoft​ Edge
  7.DevTools : true
  8.DevTools,127.0.0.1:3000/index.html : true
  input: Profession :- College student studying computer science

  Processes:
  1.test_removebrackets.py,THEAPP,Cursor
  2.Is DPN the new VPN? | Deeper Connect Air Unboxing and First Look 🔥,YouTube,Opera
  3.2023-10-29.csv,THEAPP,Cursor
  4.Quick settings
  5.Deeper Connect Air: World's Best VPN Router | Indiegogo,Opera
  6.Online Shopping site in India: Shop Online for Mobiles Books Watches Shoes and More,Amazon.in,Opera    
  7.Stremio
  8.Kaspersky Anti-Virus
  9.GlassWire
  10.System tray overflow window.
  output: 1.test_removebrackets.py,THEAPP,Cursor : true
  2.Is DPN the new VPN? | Deeper Connect Air Unboxing and First Look 🔥,YouTube,Opera : false
  3.2023-10-29.csv,THEAPP,Cursor : true
  4.Quick settings : false
  5.Deeper Connect Air: World's Best VPN Router | Indiegogo,Opera : false
  6.Online Shopping site in India: Shop Online for Mobiles Books Watches Shoes and More,Amazon.in,Opera   : false
    7.Stremio : false
  8.Kaspersky Anti-Virus : false
  9.GlassWire : false
  10.System tray overflow window. : false
  input: Profession :- College student studying computer science

  Processes:
  1.GitHub,ryanlleung/AI-Video-and-Image-Upscaling and 5 more pages,Personal,Microsoft​ Edge
  2.GitHub,k4yt3x/video2x: A lossless video/GIF/image upscaler achieved with waifu2x Anime4K SRMD and RealSR. Started in Hack the Valley II 2018. and 3 more pages,Personal,Microsoft​ Edge
  3.GitHub,k4yt3x/video2x: A lossless video/GIF/image upscaler achieved with waifu2x Anime4K SRMD and RealSR. Started in Hack the Valley II 2018. and 1 more page,Personal,Microsoft​ Edge
  4.Release Video2X 4.8.1 · k4yt3x/video2x · GitHub and 1 more page,Personal,Microsoft​ Edge
  5.GitHub,Opera
  6.Repository search results,Opera
  7.It was just a question.. 😂,YouTube,Opera
  8.Error,Opera
  9.Neil DeGrasse Tyson Destroys a RUDE Waiter with FACTS,YouTube,Opera


  output: 1.GitHub,ryanlleung/AI-Video-and-Image-Upscaling and 5 more pages,Personal,Microsoft​ Edge : true
  2.GitHub,k4yt3x/video2x: A lossless video/GIF/image upscaler achieved with waifu2x Anime4K SRMD and RealSR. Started in Hack the Valley II 2018. and 3 more pages,Personal,Microsoft​ Edge : true
  3.GitHub,k4yt3x/video2x: A lossless video/GIF/image upscaler achieved with waifu2x Anime4K SRMD and RealSR. Started in Hack the Valley II 2018. and 1 more page,Personal,Microsoft​ Edge : true
  4.Release Video2X 4.8.1 · k4yt3x/video2x · GitHub and 1 more page,Personal,Microsoft​ Edge : true
  5.GitHub,Opera : true
  6.Repository search results,Opera : false
  7.It was just a question.. 😂,YouTube,Opera : false
  8.Error,Opera : false
  9.Neil DeGrasse Tyson Destroys a RUDE Waiter with FACTS,YouTube,Opera : false

  input: Profession :- College student studying computer science

  Processes:
  10.Not -1/12,YouTube,Opera
  11.Djdefrag/QualityScaler: QualityScaler,image/video AI upscaler app,Opera
  12.Release QualityScaler 2.8 · Djdefrag/QualityScaler,Opera
  13.Picture in Picture
  14.VirusTotal,Opera
  15.VirusTotal,File,9ed731f05f82fdd8bc2a6f10494ac9b86eac6583ec09aef5809b024697116ae4,Opera
  16.sunny2109/SAFMN: [ICCV 2023] Spatially-Adaptive Feature Modulation for Efficient Image Super-Resolution; runner-up method for the model complexity track in NTIRE2023 Efficient SR challenge,Opera
  17.File Explorer
  18.QualityScaler-2.8
  output: 10.Not -1/12,YouTube,Opera : false
  11.Djdefrag/QualityScaler: QualityScaler,image/video AI upscaler app,Opera : false
  12.Release QualityScaler 2.8 · Djdefrag/QualityScaler,Opera : false
  13.Picture in Picture : false
  14.VirusTotal,Opera : false
  15.VirusTotal,File,9ed731f05f82fdd8bc2a6f10494ac9b86eac6583ec09aef5809b024697116ae4,Opera : false
  16.sunny2109/SAFMN: [ICCV 2023] Spatially-Adaptive Feature Modulation for Efficient Image Super-Resolution; runner-up method for the model complexity track in NTIRE2023 Efficient SR challenge,Opera : true
  17.File Explorer : false
  18.QualityScaler-2.8 : false
  input: Profession :- College student studying computer science

  Processes:
  100.Saas UI Element Design by Kamrul Hossain on Dribbble,Opera
  101.dribbble.com/shots/4275372-Sales-CRM-Admin-Dashboard-UI-design,Opera
  102.Sales CRM Admin Dashboard UI design by Kanmani Neha on Dribbble,Opera
  103.dribbble.com/shots/10857372-Bhulua-Bootstrap-4-Admin-Template-Deshboard,Opera
  104.Bhulua Bootstrap 4 Admin Template Deshboard by Alamin Sourav on Dribbble,Opera
  105.Untitled and 1 more page,Personal,Microsoft​ Edge
  106.How to Easily Build Desktop Apps with HTML CSS and Javascript and 1 more page,Personal,Microsoft​ Edgge
  107.Build cross-platform desktop apps with JavaScript HTML and CSS | Electron,Opera
  108.Introduction | Electron,Opera
  109.Launch in Fiddle,Opera
  110.Friends,Discord

  output: 100.Saas UI Element Design by Kamrul Hossain on Dribbble,Opera : true
  101.dribbble.com/shots/4275372-Sales-CRM-Admin-Dashboard-UI-design,Opera : true
  102.Sales CRM Admin Dashboard UI design by Kanmani Neha on Dribbble,Opera : true
  103.dribbble.com/shots/10857372-Bhulua-Bootstrap-4-Admin-Template-Deshboard,Opera : true
  104.Bhulua Bootstrap 4 Admin Template Deshboard by Alamin Sourav on Dribbble,Opera : true
  105.Untitled and 1 more page,Personal,Microsoft​ Edge : false
  106.How to Easily Build Desktop Apps with HTML CSS and Javascript and 1 more page,Personal,Microsoft​ Edgge : true
  107.Build cross-platform desktop apps with JavaScript HTML and CSS | Electron,Opera : true
  108.Introduction | Electron,Opera : true
  109.Launch in Fiddle,Opera : false
  110.Friends,Discord : false
  input: Profession :- College student studying computer science

  Processes:
  108.Introduction | Electron,Opera
  109.Launch in Fiddle,Opera
  110.Friends,Discord
  111.#for_the_vmsians | Onli SRL,Discord
  112.#free-games | VulTuRe,Discord
  113.electron/docs/fiddles/quick-start at v27.0.2 · electron/electron,Opera
  114.Electron Fiddle | Electron,Opera
  115.Getting Started,Electron Forge,Opera
  116.Quick Start | Electron,Opera

  output: 108.Introduction | Electron,Opera : true
  109.Launch in Fiddle,Opera : false
  110.Friends,Discord : false
  111.#for_the_vmsians | Onli SRL,Discord : false
  112.#free-games | VulTuRe,Discord : false
  113.electron/docs/fiddles/quick-start at v27.0.2 · electron/electron,Opera : true
  114.Electron Fiddle | Electron,Opera : true
  115.Getting Started,Electron Forge,Opera : true
  116.Quick Start | Electron,Opera : true
  input: Profession :- College student studying computer science

  Processes:
  1.test_removebrackets.py,SAI AND SE 5th sem,Cursor
  2.graph.js,SAI AND SE 5th sem,Cursor
  3.2023-11-05.csv,SAI AND SE 5th sem,Cursor
  4.PaLM API  |  Generative AI for Developers,Opera
  5.Speed Dial,Opera
  6.YouTube,Opera
  7.Quick settings
  8.12 CHUTKULE | Gaurav Kapoor | Stand Up Comedy | Short Jokes Compilation,YouTube,Opera
  9.Task Manager
  10.This drama is insane,YouTube,Opera



  output: 1.test_removebrackets.py,SAI AND SE 5th sem,Cursor : true
  2.graph.js,SAI AND SE 5th sem,Cursor : true
  3.2023-11-05.csv,SAI AND SE 5th sem,Cursor : true
  4.PaLM API  |  Generative AI for Developers,Opera : true
  5.Speed Dial,Opera : false
  6.YouTube,Opera : false
  7.Quick settings : false
  8.12 CHUTKULE | Gaurav Kapoor | Stand Up Comedy | Short Jokes Compilation,YouTube,Opera : false
  9.Task Manager : false
  10.This drama is insane,YouTube,Opera : false


  input: Profession :- College student studying computer science

  Processes:
  11.super super,YouTube,Opera
  12.SuperSuper,YouTube,Opera
  13.I am KANG! | Kang edit | Hensonn Flare | Ant-Man and the Wasp Quantumania,YouTube,Opera
  14.Its rollin at the top,YouTube,Opera
  15.A Real Authentic Mexican,YouTube,Opera
  16.Which is the best Transformation Marvel Vs Dc | Rune Edits Version | #shorts #marvel #dc #avengers,YouTube,Opera
  17.😱 The best offer in Shark tank 🔥 #shorts #motivation,YouTube,Opera
  18.Eastern vs Western Numerals,YouTube,Opera
  19.ULTIMATE LIFEHACKS 🤩 #2,YouTube,Opera
  20.Sasuke edit/@Sasuke_uchiha57,YouTube,Opera
  output: 11.super super,YouTube,Opera : false
  12.SuperSuper,YouTube,Opera : false
  13.I am KANG! | Kang edit | Hensonn Flare | Ant-Man and the Wasp Quantumania,YouTube,Opera : false
  14.Its rollin at the top,YouTube,Opera : false
  15.A Real Authentic Mexican,YouTube,Opera : false
  16.Which is the best Transformation Marvel Vs Dc | Rune Edits Version | #shorts #marvel #dc #avengers,YouTube,Opera : false
  17.😱 The best offer in Shark tank 🔥 #shorts #motivation,YouTube,Opera : false
  18.Eastern vs Western Numerals,YouTube,Opera : false
  19.ULTIMATE LIFEHACKS 🤩 #2,YouTube,Opera : false
  20.Sasuke edit/@Sasuke_uchiha57,YouTube,Opera : false
  input: Profession :- College student studying computer science

  Processes:
  21.odin collected the infinity stones before thanos in mcu #shorts,YouTube,Opera
  22.Boom Doppda Boom,YouTube,Opera
  23.The last joke will make you laugh,YouTube,Opera
  24.Wolf Of Wall Street 😂,YouTube,Opera
  25.Visual opiates are all around you #shorts,YouTube,Opera

  output: 21.odin collected the infinity stones before thanos in mcu #shorts,YouTube,Opera : false
  22.Boom Doppda Boom,YouTube,Opera : false
  23.The last joke will make you laugh,YouTube,Opera : false
  24.Wolf Of Wall Street 😂,YouTube,Opera : false
  25.Visual opiates are all around you #shorts,YouTube,Opera : false

  input: Profession :- College student studying computer science

  Processes:
  26.Would YOU survive in WARZONE 2.0?!,YouTube,Opera
  27.LOKI Season 2 Episode 1 Easter Egg Part 1 #shorts,YouTube,Opera
  28.November 4 2023,YouTube,Opera
  29.Sword thru neck secret explained! 😲,YouTube,Opera
  30.Am I wrong? 😬 #shorts,YouTube,Opera
  31.Search
  32.Wait for @misupubg #short#bgmi#victor#pubg,YouTube,Opera

  output: 26.Would YOU survive in WARZONE 2.0?!,YouTube,Opera : false
  27.LOKI Season 2 Episode 1 Easter Egg Part 1 #shorts,YouTube,Opera : false
  28.November 4 2023,YouTube,Opera : false
  29.Sword thru neck secret explained! 😲,YouTube,Opera : false
  30.Am I wrong? 😬 #shorts,YouTube,Opera : false
  31.Search : false
  32.Wait for @misupubg #short#bgmi#victor#pubg,YouTube,Opera : false

  input: Profession :- College student studying computer science

  Processes:
  33.Loki vs Kang: The Fear You Didn't Expect. 🤯🔥 #loki #shorts #youtubeshorts,YouTube,Opera
  34.Google Translate to French!?,YouTube,Opera
  35.english to french trsaaltion,Google Search,Opera
  36.The last girl wasn’t leaving without her money,YouTube,Opera
  37.Sigma saves a cat,YouTube,Opera
  38.Spicy Beatbox Challenge #beatbox #tiktok,YouTube,Opera
  39.Just click #viral #shorts #short,YouTube,Opera
  40.How to fix a sword hole in the wall 🗡,YouTube,Opera

  output: 33.Loki vs Kang: The Fear You Didn't Expect. 🤯🔥 #loki #shorts #youtubeshorts,YouTube,Opera : false
  34.Google Translate to French!?,YouTube,Opera : false
  35.english to french trsaaltion,Google Search,Opera : false
  36.The last girl wasn’t leaving without her money,YouTube,Opera : false
  37.Sigma saves a cat,YouTube,Opera : false
  38.Spicy Beatbox Challenge #beatbox #tiktok,YouTube,Opera : false
  39.Just click #viral #shorts #short,YouTube,Opera : false
  40.How to fix a sword hole in the wall 🗡,YouTube,Opera : false
  input: Profession :- College student studying computer science

  Processes:
  41.The Moment Loki Realised Infinity Stones are useless 💔🥺 #shorts #viral #loki #trending #marvel,YouTube,Opera
  42.THE END was SO EMBARRASSING 😂 @RegalNoise #hannahandregal #couple #relationship #funny #comedy,YouTube,Opera
  43.With my friend #vrindavan #ytshorts #motivation #shortsfeed #reels #cortoon,YouTube,Opera
  44.POV: You're In Siblings or Dating Class | #clips #twitch,YouTube,Opera
  45.Lebanese dad jokes at its finest,YouTube,Opera
  46.Facing Off in Professional Air Hockey #airhockey #arcade,YouTube,Opera


  output: 41.The Moment Loki Realised Infinity Stones are useless 💔🥺 #shorts #viral #loki #trending #marvel,YouTube,Opera : false
  42.THE END was SO EMBARRASSING 😂 @RegalNoise #hannahandregal #couple #relationship #funny #comedy,YouTube,Opera : false
  43.With my friend #vrindavan #ytshorts #motivation #shortsfeed #reels #cortoon,YouTube,Opera : false
  44.POV: You're In Siblings or Dating Class | #clips #twitch,YouTube,Opera : false
  45.Lebanese dad jokes at its finest,YouTube,Opera : false
  46.Facing Off in Professional Air Hockey #airhockey #arcade,YouTube,Opera : false


  input: Profession :- College student studying computer science

  Processes:
  47.Rule number 51. #motivation #quotes #moneymindset #inspiration #wealthfreedom #shorts #mindset,YouTube,Opera
  48.A Real Authentic Italian,YouTube,Opera
  49.Arnold Schwarzenegger's Story: The Changing Tides of Fame #motivation #arnoldschwarzenegger #shorts,YouTube,Opera
  50.Sound effects of Squid Game #beatbox #tiktok,YouTube,Opera
  51.WHEN KURUMA TOOK JUSTICE IN HIS OWN HANDS🔥🥵•|#shorts #naruto,YouTube,Opera
  52.Woke Feminist RUNS AWAY From Candace Owens,YouTube,Opera
  53.Tobey Maguire Sigma Gets his revenge :) 4K,YouTube,Opera
  output: 47.Rule number 51. #motivation #quotes #moneymindset #inspiration #wealthfreedom #shorts #mindset,YouTube,Opera : false
  48.A Real Authentic Italian,YouTube,Opera : false
  49.Arnold Schwarzenegger's Story: The Changing Tides of Fame #motivation #arnoldschwarzenegger #shorts,YouTube,Opera : false
  50.Sound effects of Squid Game #beatbox #tiktok,YouTube,Opera : false
  51.WHEN KURUMA TOOK JUSTICE IN HIS OWN HANDS🔥🥵•|#shorts #naruto,YouTube,Opera : false
  52.Woke Feminist RUNS AWAY From Candace Owens,YouTube,Opera : false
  53.Tobey Maguire Sigma Gets his revenge :) 4K,YouTube,Opera : false
  input: Profession :- College student studying computer science

  Processes:
  56.#JasonDeruloTV // Satisfying Machine Shredder #SlowLow,YouTube,Opera
  57.Make me laugh challenge gone wrong,YouTube,Opera
  61.Destroy the Orange Ball,YouTube,Opera
  62.Elemental 4k Edit,YouTube,Opera
  63.Feminists Really Tried To Cancel A VIDEOGAME,YouTube,Opera
  64.TikTok Family Fakes Height for Views and Money #shorts,YouTube,Opera
  65.WHY THERE ARE NO X-MENS IN THE MCU? | X-MEN | AVENGERS | #marveluniverse #marvelcomics #shorts,YouTube,Opera
  66.Pictures Taken Moments Before Tragedy 😳,YouTube,Opera
  67.How to win and lose on Feud at the same time. #shorts,YouTube,Opera
  68.Windscribe
  69.Epic Games Launcher
  output: 56.#JasonDeruloTV // Satisfying Machine Shredder #SlowLow,YouTube,Opera : false
  57.Make me laugh challenge gone wrong,YouTube,Opera : false
  61.Destroy the Orange Ball,YouTube,Opera : false
  62.Elemental 4k Edit,YouTube,Opera : false
  63.Feminists Really Tried To Cancel A VIDEOGAME,YouTube,Opera : false
  64.TikTok Family Fakes Height for Views and Money #shorts,YouTube,Opera : false
  65.WHY THERE ARE NO X-MENS IN THE MCU? | X-MEN | AVENGERS | #marveluniverse #marvelcomics #shorts,YouTube,Opera : false
  66.Pictures Taken Moments Before Tragedy 😳,YouTube,Opera : false
  67.How to win and lose on Feud at the same time. #shorts,YouTube,Opera : false
  68.Windscribe : false
  69.Epic Games Launcher : false
  input: Profession :- College student studying computer science

  Processes:
  51.The girls at the end made my day,make me laugh challenge,YouTube,Opera
  52.6ix9ine DISSED Lil Mabu #shorts #6ix9ine #lilmabu #disstrack,YouTube,Opera
  53.Why Was India ONCE Known To Be 'Sone Ki Chidiya' #shorts,YouTube,Opera
  54.Quit Opera?
  55.mongodbtest.py,THEAPP,Cursor
  56.2023-10-27.csv,THEAPP,Cursor
  57.2023-10-26.csv,THEAPP,Cursor
  58.activity_data.csv,THEAPP,Cursor
  59.Bing Chat with GPT-4,Personal,Microsoft​ Edge
  60.,Opera
  61.GX Corner,Opera
  62.YouTube,Opera
  63.MongoDB Compass,localhost:27017/THEAPP.2023-10-28
  output: 51.The girls at the end made my day,make me laugh challenge,YouTube,Opera : false
  52.6ix9ine DISSED Lil Mabu #shorts #6ix9ine #lilmabu #disstrack,YouTube,Opera : false
  53.Why Was India ONCE Known To Be 'Sone Ki Chidiya' #shorts,YouTube,Opera : false
  54.Quit Opera? : false
  55.mongodbtest.py,THEAPP,Cursor : true
  56.2023-10-27.csv,THEAPP,Cursor : true
  57.2023-10-26.csv,THEAPP,Cursor : true
  58.activity_data.csv,THEAPP,Cursor : true
  59.Bing Chat with GPT-4,Personal,Microsoft​ Edge : false
  60.,Opera : false
  61.GX Corner,Opera : false
  62.YouTube,Opera : false
  63.MongoDB Compass,localhost:27017/THEAPP.2023-10-28 : true
  input: Profession :- College student studing computer science

  Processes:
  1.test_removebrackets.py,SAI AND SE 5th sem,Cursor
  2.index.html,SAI AND SE 5th sem,Cursor
  3.2023-11-04.csv,SAI AND SE 5th sem,Cursor
  4.GlassWire
  5.Daily Activity Tracking,Opera
  6.Speed Dial,Opera
  7.youtube.com,Opera
  8.YouTube,Opera
  9.Time Tracking and Management,Opera
  10.Windows Default Lock Screen
  11.UnlockingWindow
  12.SAI GROUP 18 5th sem .pptx,WPS Office

  output: 1.test_removebrackets.py,SAI AND SE 5th sem,Cursor : true
  2.index.html,SAI AND SE 5th sem,Cursor : true
  3.2023-11-04.csv,SAI AND SE 5th sem,Cursor : true
  4.GlassWire : false
  5.Daily Activity Tracking,Opera : false
  6.Speed Dial,Opera : false
  7.youtube.com,Opera : false
  8.YouTube,Opera : false
  9.Time Tracking and Management,Opera : false
  10.Windows Default Lock Screen : false
  11.UnlockingWindow : false
  12.SAI GROUP 18 5th sem .pptx,WPS Office : true

  input: Profession :- College student studing computer science

  Processes:
  13.WPS Presentation Slide Show,[SAI GROUP 18 5th sem .pptx]
  14.Save
  15.Quick settings
  16.SAI GROUP 18 5th sem FINAL.pptx,WPS Office
  17.WPS Presentation Slide Show,[SAI GROUP 18 5th sem FINAL.pptx]
  18.Save As
  19.SAI GROUP 18 5th sem EKDAM FINAL.pptx,WPS Office
  20.Confirm Save As
  21.Presentation
  22.WPS Office
  23.SAI GROUP 18 FINAL REPORT.docx,WPS Office
  24.Open
  output: 13.WPS Presentation Slide Show,[SAI GROUP 18 5th sem .pptx] : true
  14.Save : false
  15.Quick settings : false
  16.SAI GROUP 18 5th sem FINAL.pptx,WPS Office : true
  17.WPS Presentation Slide Show,[SAI GROUP 18 5th sem FINAL.pptx] : true
  18.Save As : false
  19.SAI GROUP 18 5th sem EKDAM FINAL.pptx,WPS Office : true
  20.Confirm Save As : false
  21.Presentation : false
  22.WPS Office : false
  23.SAI GROUP 18 FINAL REPORT.docx,WPS Office : true
  24.Open : false
  input: Profession :- College student studing computer science

  Processes:
  1.test_removebrackets.py,SAI AND SE 5th sem,Visual Studio Code
  2.gs_style.css,SAI AND SE 5th sem,Visual Studio Code
  3.index.html,SAI AND SE 5th sem,Visual Studio Code
  4.Quick settings
  5.Time Tracking and Management,Google Chrome
  6.Daily Activity Tracking,Google Chrome
  7.New Tab,Google Chrome
  8.YouTube,Google Chrome
  9.Ye Best Patakha hai 😂 Maza Aagya,YouTube,Google Chrome
  10.tldr.teech,Google Search,Google Chrome
  11.TLDR Newsletter,A Byte Sized Daily Tech Newsletter,Google Chrome
  12.udemy,Google Search,Google Chrome
  13.Online Courses,Learn Anything On Your Schedule | Udemy,Google Chrome
  14.Search results | Udemy,Google Chrome
  15.figma,Google Search,Google Chrome
  16.Figma: The Collaborative Interface Design Tool,Google Chrome
  17.Bookmark added
  18.web dev simplifued,YouTube,Google Chrome
  19.telosko,YouTube,Google Chrome
  20.react web dev simplifued,YouTube,Google Chrome
  21.mosh hamedani react,YouTube,Google Chrome
  22.tesko react,YouTube,Google Chrome
  23.telesko react,YouTube,Google Chrome
  24.Almost done you're so close! 🤏,Google Chrome
  25.Search
  26.Windows Default Lock Screen
  27.UnlockingWindow

  output: 1.test_removebrackets.py,SAI AND SE 5th sem,Visual Studio Code : true
  2.gs_style.css,SAI AND SE 5th sem,Visual Studio Code : true
  3.index.html,SAI AND SE 5th sem,Visual Studio Code : true
  4.Quick settings : false
  5.Time Tracking and Management,Google Chrome : false
  6.Daily Activity Tracking,Google Chrome : false
  7.New Tab,Google Chrome : false
  8.YouTube,Google Chrome : false
  9.Ye Best Patakha hai 😂 Maza Aagya,YouTube,Google Chrome : false
  10.tldr.teech,Google Search,Google Chrome : false
  11.TLDR Newsletter,A Byte Sized Daily Tech Newsletter,Google Chrome : false
  12.udemy,Google Search,Google Chrome : true
  13.Online Courses,Learn Anything On Your Schedule | Udemy,Google Chrome : true
  14.Search results | Udemy,Google Chrome : true
  15.figma,Google Search,Google Chrome : true
  16.Figma: The Collaborative Interface Design Tool,Google Chrom : true
  17.Bookmark added : false
  18.web dev simplifued,YouTube,Google Chrome : true
  19.telosko,YouTube,Google Chrome : true
  20.react web dev simplifued,YouTube,Google Chrome  : true
  21.mosh hamedani react,YouTube,Google Chrome : false
  22.tesko react,YouTube,Google Chrome : true
  23.telesko react,YouTube,Google Chrome : true
  24.Almost done you're so close! 🤏,Google Chrome : false
  25.Search : false
  26.Windows Default Lock Screen : false
  27.UnlockingWindow : false

  input: Profession :- College student studing computer science

  Processes:
  28.Untitled,Google Chrome
  29.SAGNIK-Dev-portfolio,Google Chrome
  30.Local Disk
  31.sign_style.css,SAI AND SE 5th sem,Visual Studio Code
  32.Error,Google Chrome
  33.Microsoft Store
  34.Sourav Joshi Vlogs,YouTube,Google Chrome
  35.tlesko,YouTube,Google Chrome
  36.telesko,YouTube,Google Chrome
  37.web dev simplified react,YouTube,Google Chrome
  38.Rajasthan के Kota में Chambal River Front विदेशों को टक्कर देता है क्या Gehlot को फ़ायदा होगा?,         ,YouTube,Google Chrome
  39.Aisa Machher Jhol Life Mein Nahi Khaya 🐟🦐🤤 | Siliguri Ep.2 @zerowattfilms,YouTube,Google Chrome
  40.Program Manager

  output: 28.Untitled,Google Chrome : false
  29.SAGNIK-Dev-portfolio,Google Chrome : false
  30.Local Disk : false
  31.sign_style.css,SAI AND SE 5th sem,Visual Studio Code : true
  32.Error,Google Chrome : false
  33.Microsoft Store : false
  34.Sourav Joshi Vlogs,YouTube,Google Chrome : false
  35.tlesko,YouTube,Google Chrome : true
  36.telesko,YouTube,Google Chrome : true
  37.web dev simplified react,YouTube,Google Chrome : true
  38.Rajasthan के Kota में Chambal River Front विदेशों को टक्कर देता है क्या Gehlot को फ़ायदा होगा?,         ,YouTube,Google Chrome : false
  39.Aisa Machher Jhol Life Mein Nahi Khaya 🐟🦐🤤 | Siliguri Ep.2 @zerowattfilms,YouTube,Google Chrome : false
  40.Program Manager : false
  input: Profession :- College student studying computer science
  Processes:
  1.C:\WINDOWS\py.exe
  2.SAI AND SE 5th sem
  3.Daily Activity Tracking,Google Chrome
  4.38. JS Basics,Class I [HD],VLC media player
  5.Windows Default Lock Screen6.Program Manager
  output: 1.C:\WINDOWS\py.exe : false
  2.SAI AND SE 5th sem : true
  3.Daily Activity Tracking,Google Chrome : false
  4.38. JS Basics,Class I [HD],VLC media player : true
  5.Windows Default Lock Screen6.Program Manager : false
  input: {input}
  output:"""

def ai_api(input):
  response = genai.generate_text(
    **defaults,
    prompt=prompt(input)
  )

  return response.result
  
  
path = input("Enter Date: ")
pathai = path + "_AI_Evaluated"
  
csv_data_string = dtp.csvdata(path+'.csv')
print(csv_data_string)
# Split the string into lines
lines = csv_data_string.split('\n')

# Create an array to store the lines in groups of 20
lines_array = [lines[i:i+20] for i in range(0, len(lines), 20)]

# Print or use the resulting array
for group in lines_array:
  
  processes = ('\n'.join(group))
  proffession = "Profession :- College student studying computer science"
  input = proffession + "\nProcesses:\n" + processes + ":"
  ai_data = ai_api(input)
  print(ai_data)
  with open(pathai+'.csv', 'a',encoding='utf-8') as f:
    f.write(ai_data)
    f.write("\n")
    f.close()
  
  
ptd.replace_word_in_csv(pathai+'.csv')