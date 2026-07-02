Ishlatish:
Agar sen avvalgi retime.py orqali chiqargan expanded_script.txt bilan tekshirmoqchi bo'lsang (script sening formulang bilan, audio esa haqiqiy fayl):
bashpython main.py --audio narration.mp3 --script expanded_script.txt
Yoki, agar Whisper'ga audio'ni to'g'ridan-to'g'ri berib, haqiqiy so'z darajasidagi timing'ni olishni xohlasang (bu yerda mening formulam ishlatilmaydi — Whisper audio'ning o'zidan aniq vaqtni o'qiydi):
bashpython main.py --audio narration.mp3 --transcribe
Ikkinchi variant senga foydali bo'ladi — chunki shu orqali expanded_script.txtdagi formulaviy taxminlarni haqiqiy audio bilan solishtirib, formulani qanchalik to'g'ri ishlayotganini baholay olasan.
Eslatma: --transcribe rejimida birinchi ishga tushirishda Whisper modelini yuklab oladi (small — bir necha yuz MB), shuning uchun birinchi safar biroz sekinroq bo'ladi. Tezlik/aniqlik nisbatini o'zgartirmoqchi bo'lsang, transcribe_audio() ichidagi model_size ni "tiny", "base", "medium" yoki "large" ga almashtirasan.