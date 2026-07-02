# Ishlatish:
Agar sen avvalgi retime.py orqali chiqargan expanded_script.txt bilan tekshirmoqchi bo'lsang (script sening formulang bilan, audio esa haqiqiy fayl):
python main.py --audio narration.mp3 --script expanded_script.txt

Yoki, agar Whisper'ga audio'ni to'g'ridan-to'g'ri berib, haqiqiy so'z darajasidagi timing'ni olishni xohlasang (bu yerda mening formulam ishlatilmaydi — Whisper audio'ning o'zidan aniq vaqtni o'qiydi):
bashpython main.py --audio narration.mp3 --transcribe

Ikkinchi variant senga foydali bo'ladi — chunki shu orqali expanded_script.txt dagi formulaviy taxminlarni haqiqiy audio bilan solishtirib, formulani qanchalik to'g'ri ishlayotganini baholay olasan.

Eslatma: --transcribe rejimida birinchi ishga tushirishda Whisper modelini yuklab oladi (small — bir necha yuz MB), shuning uchun birinchi safar biroz sekinroq bo'ladi. Tezlik/aniqlik nisbatini o'zgartirmoqchi bo'lsang, transcribe_audio() ichidagi model_size ni "tiny", "base", "medium" yoki "large" ga almashtirasan.

# Eslatma:
Agar proyekt terminalda ishlashida kamchilik chiqadigan bo'lsa,
terminalda Exlatma.txt da yozilgan cmd larni navbati bilan kiritib ko'r.

# So'nngi ishlatish yo'riqnomasi:

# Proyektgacha .mp3 va timed .txt fayl tayyorlash:
1. biror mavzuda kichik qismga bo'lib bo'lib audio yozib olinadi. 
Any voice rec app on mobile or PC
(Barcha audio qismlari sifatli o'qilishi shart.)
2. yozib olingan kichik qismli nomida tartib raqami bor audio Voice Rec folderga joylanadi.
3. har bir audiodan audio trimmer sayt orqali boshi va oxiridagi pauzalar kesib qayta 
Trimmed folderga yuklab olinadi. 
https://audiotrimmer.com/
4. Barcha trimmed audioni tartib raqami bo'yicha merge qilib, eshtib ko'riladi va matn bilan solishtiriladi va audioga nom berib saqlab qo'yiladi.
https://clideo.com/merge-audio
5. Hosil bo'lgan audioni turboscribe sayti orqali whale tezligida transcribsiya qilib, timingli matnidan to'liq nusxa olinadi va transcribe.txt deb saqlab qo'yiladi. Va eng oxirida audio uzunligi timingni ko'rib masalan audio (6:10)daqiqa bo'lsa, bu time stampni input_script.txt eng oxirida "(6:10) The End." shaklda yozish shart. (Aks holda video oxiri sifatsiz chiqadi.)

# (5.) da hosil bo'lgan .txt faylni joriy proyektda ishlatish: (Maqsad video kadrlar sonini sezilarli sonda (4-5 martaga) oshirish)
6. input_script.txt faylini ichiga (5.) da hosil bo'lgan .txt fayl copy + paste qilinadi.
7. CMD => "cd out-test" folderga o'tiladi.
8. CMD => "./exp.sh" orqali script qayta retiming qilinadi bunda script 3 sekundli interval darajasida qayta yoziladi va kengayadi.
9. natija fayl: out-text/data/expanded_script.txt. olingan natijani Claude Ai bilan davom ettiriladi.

# Claude ai orqali qayta tartiblash: (Maqsad retiming qilingan txt uchun higgsfiled automat extensionga mos prompt set tayyorlash.)
10. Claude da yangi oyna ochish.
11. oynaga joriy proyektdagi Claude/static-starting folder ichidagi "initStd.txt" va Technics-Exp-Deepseek.txt" fayllarni joylash va mainPrompt.txt ni chat qismiga copy + paste qilish.
12. Claude yoki javob beradi yoki bizdan quyidagicha so'rashi mumkin:
    Q: Promptlarni qanday tartibda tayyorlashimni xohlaysiz?
    A: 1 daqiqalik bo'laklarga bo'lib (0:00-1:00, keyin 1:00-2:00...) "S0:00T" formatda timing + har bir prompr bir biridan bir qator bo'sh joy bilan ajratilgan holatda
    (Bu tahrirlanganprompt)
(Juda yuqori muhim qism: agar claude "S0:00T" standartda boshlangan promptlar taqdim qilmasa, bu keyinchalik, (20) ishlamasligiga olib keladi.)    
13. Sifat yuqori bo'lishi u-n Claudedan har safar 1 daqiqa keyinni generatsiya qilishini so'raymiz:
    prompt:
    keyingi qism>
14. olgan barcha timing qismli promptlarni Claude/responseTest-xxx.txt fayliga tartib bilan keraksiz matnlardan xoli hamda bir qator bo'sh joy tashlangan standart shaklida saqlaymiz.

# HIggsfield img gen automation:
15. Higgsfield ai image qismiga o'tib, "Seedream4.5" image gen model tanlaymiz (unlimited bo'lgani u-n) va tiniqlik 4k, ratio: 16:9, (bu juda muhim) unlimited on qilib sozlaymiz.
16. HIggsfiled automation Chrome Extensionda ham sozlamalar qilamiz:
    setting:
    1. Default Mode => Text To Img
    2. Max Retries on Failure => 3
    3. Save Settings
    control
    1. Concurrent Prompts => 4
    2. Random Delay => (5-11)
    3. Outputs per Prompt => 1
    if need
    4. Save to folder => Any name depend of topic title
17. sozlama tekshiriladi, (15) juda yaxshilab tekshiriladi.
18. Chrome Extensionga prompt maydoniga (14) txt nusxasi tashlanib, prompt soni eslab qolinadi.
19. (14) dagi promptlar soni bilan mos kelishi tekshiriladi.

# kechasi bilan img auto gen yoqib qo'yish:
20. Run berilib miqdoriga qarab 5 soat + atrofida kutiladi (100ta rasmdan ko'p odatda)
21. Agar rasm 100tadan kam bo'lsa normal davom et, aks holda keyingi qadam:
22. dw-higgs-png folderga kirish va CMD: "./download.sh" ni buyurish.
(bunda folderdagi rasmlar keraksizligiga ishoch hosil qiling chunki clean qilinadi)
23. ha deb yozish, oxirgi n ta rasmlar kerakligini yani n ni kiritish.
(Max 100 ta rasm mumkin. Agar ko'p bo'lsa, N = 100 kiritish, yuklanishini kutish keyin 
    saytda:
    manual Higgsfield sahifasida oxirgi 100 ta rasmni delete qilish
24. lokalda esa:
    olingan 100 (n) ta rasmni dw folderdan out folderga ko'chirish kerak.)

# Natijani kuzatish:
25. out folderda CMD => "./main.sh" terish.

(main.sh va exp.sh lar har doim audio va script yangilanganda fayl nomiga mos o'zgarishi shart)