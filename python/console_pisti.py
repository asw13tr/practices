import time
import random

# KART SINIFI
class Kart():
    def __init__(self, simge, icon, numara, puan) -> None:
        #self.id = "{}_{}_{}".format(simge, numara, puan)
        self.isim = """[{}] {}""".format(icon, numara)
        self.simge = simge
        self.icon = icon
        self.numara = numara
        self.puan = puan


# OYUNCU SINIFI
class Oyuncu():
    def __init__(self, isim, index=None) -> None:
        self.index = index
        self.isim = isim
        self.puan = 0
        self.kartlar = []
        self.kazandigiKartlar = []
        self.pisti = 0


# DEĞİŞKENLER OLUŞTURMA
listeSimgeler = {
    'MAÇA': '♠',
    'KUPA': '♥',
    'KARO': '♦',
    'SİNEK': '♣',
}
listeSayilar = ('A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K')
listeKartlar = [] #1,
bosKart = Kart("", "-", "YOK", 0)

for (simge, icon) in listeSimgeler.items(): # simge = MAÇA, icon=♠
    for sayi in listeSayilar:
        puan=1
        if sayi=='J':
            puan=10

        yeniKart = Kart(simge, icon, sayi, puan)
        listeKartlar.append(yeniKart)




# KARIŞTIRMA FONKSİYONU
def kartlariKaristir(kartlar):
    kartSayisi = len(kartlar)
    parcaSayisi = int(kartSayisi / 4)
    
    deste1 = kartlar[(0) : (0+parcaSayisi)] #♠
    deste2 = kartlar[(parcaSayisi*1) : ((parcaSayisi*1)+parcaSayisi)]
    deste3 = kartlar[(parcaSayisi*2) : ((parcaSayisi*2)+parcaSayisi)]
    deste4 = kartlar[(parcaSayisi*3) : ((parcaSayisi*3)+parcaSayisi)]

    random.shuffle(deste1)
    random.shuffle(deste2)
    random.shuffle(deste3)
    random.shuffle(deste4)
    
    deste1.extend(deste2)
    deste3.extend(deste4)

    random.shuffle(deste1)
    random.shuffle(deste3)

    deste1.extend(deste3)
    random.shuffle(deste1)

    return deste1




def ekranaYaz(text):
    print("\n=========================================")
    print(text)


# OYUN
class Oyun():
    kartlar = []
    yerdekiKartlar = []
    oyuncular = [] #1.oyuncu, 2.oyuncu
    sonKazananIndex = -1

    # OYUNA KATILACAK OYUNCULARI OLUŞTUR
    def oyuncuOlustur(self):
        for i in range(1,3):
            ekranaYaz("{}. Oyuncu Adını Gir".format(i))
            oyuncuAdi = input(": ").capitalize()
            yeniOyuncu = Oyuncu(oyuncuAdi, i-1)
            self.oyuncular.append( yeniOyuncu )
        ekranaYaz("OYUNCULAR HAZIR")
        print("[{}] < vs > [{}]".format(self.oyuncular[0].isim, self.oyuncular[1].isim))


    # KART DESTESİNİ KARIŞTIR VE MASAYA GETİR.
    def kartlariOlustur(self):
        ekranaYaz("→ KARTLAR KARIŞTIRILIYOR")
        #time.sleep(1)
        self.kartlar = kartlariKaristir(listeKartlar)
        ekranaYaz("→ KARTLAR HAZIR")


    # OYUNCULARA EŞİT SAYIDA KART DAĞIT
    def kartlariDagit(self):
        ekranaYaz("→ KARTLAR DAĞITILIYOR")
        #time.sleep(1)
        for tur in range(4):
            for oyuncu in self.oyuncular:
                oyuncu.kartlar.append( self.kartlar.pop() ) #maça3
        print("-> DAĞITILMAYAN KART SAYISI : ", len(self.kartlar))
    

    

    # TUR OYNA
    def turOyna(self):
        for turSayisi in range(1, 5):
            for oynayanOyuncu in self.oyuncular:
                
                sonKart = bosKart
                if len(self.yerdekiKartlar)>0:
                    sonKart = self.yerdekiKartlar[-1]

                screenTitle  = "┌────────────────────────────────────────────────────────────────┐"
                screenTitle += "\n├> TUR      : {}  -> OYUNCU   : {}"
                screenTitle += "\n├> SON KART : {}"
                screenTitle += "\n└────────────────────────────────────────────────────────────────┘"
                ekranaYaz(screenTitle.format(turSayisi, oynayanOyuncu.isim, sonKart.isim))

                for index in range(len(oynayanOyuncu.kartlar)):
                    kart = oynayanOyuncu.kartlar[index]
                    print( "({}) -> {}".format(index+1, kart.isim) )
                
                while True:
                    kartIndex = input("Kart At: ")
                    if kartIndex in ["1", "2", "3", "4"]:
                        kartIndex =  int(kartIndex)
                        break
                    

                atilanKart = oynayanOyuncu.kartlar[kartIndex-1]
                del oynayanOyuncu.kartlar[kartIndex-1]
                self.yerdekiKartlar.append(atilanKart) 

                if atilanKart.puan==10:
                    self.turKazanildi(oynayanOyuncu)
                elif atilanKart.numara==sonKart.numara:
                    if len(self.yerdekiKartlar)==2:
                        self.turKazanildi(oynayanOyuncu, True)
                    else:
                        self.turKazanildi(oynayanOyuncu)
                else:
                    pass
        else:
            if len(self.kartlar)>0:
                self.kartlariDagit()
                self.turOyna()
            else:
                self.turKazanildi(self.oyuncular[self.sonKazananIndex])
                ekranaYaz("OYUN BİTTİ")
                self.puanHesapla()
            

    # TUR KAZANILDIĞINDA OYUNCUYA KARTLARI VE PUANINI VER
    def turKazanildi(self, oynayanOyuncu, pisti=False):
        self.sonKazananIndex = oynayanOyuncu.index
        if pisti==True:
            oynayanOyuncu.pisti = oynayanOyuncu.pisti + 1
            print("Tebrikler: {} pişti yaptın.".format(oynayanOyuncu.isim))
        else:
            oynayanOyuncu.kazandigiKartlar.extend(self.yerdekiKartlar)
            print("Tebrikler: {} kartları aldın".format(oynayanOyuncu.isim))
        self.yerdekiKartlar.clear()


    # OYUN BİTTİKTEN SONRA PUANLARI HESAPLA
    def puanHesapla(self):
        for oyuncu in self.oyuncular:
            oyuncu.puan = oyuncu.pisti * 20
            for kart in oyuncu.kazandigiKartlar:
                oyuncu.puan = oyuncu.puan + kart.puan

        kazananOyuncu = self.oyuncular[0]
        for oyuncu in self.oyuncular:
            if oyuncu.puan > kazananOyuncu.puan:
                kazananOyuncu = oyuncu

        ekranaYaz("OYUN TAMAMLANDI")
        print("KAZANAN OYUNCU: " + kazananOyuncu.isim)
        print("PUAN: ", kazananOyuncu.puan)
        print("ELDE ETTİĞİ KARTLAR")
        for kart in kazananOyuncu.kazandigiKartlar:
            print("{} => {} Puan".format(kart.isim, kart.puan))
        
        print("YERDEKI KARTLAR", len(self.yerdekiKartlar))
        for kart in self.yerdekiKartlar:
            print(kart.isim)



    # OYUNA BAŞLA
    def basla(self):
        self.oyuncuOlustur()
        self.kartlariOlustur()
        self.kartlariDagit()
        
        # Yere 4 kart ekle
        for i in range(4):
            self.yerdekiKartlar.append( self.kartlar.pop() )

        print("-> DAĞITILMAYAN KART SAYISI : ", len(self.kartlar))

        self.turOyna()

            
        
        



while True:
    ekranaYaz("İŞLEM SEÇ: \n[S]=>Oyunu Başlat | [Q]=>Çıkış Yap")
    islemKarakteri = input("Girdi: ").upper()
    if "Q" in islemKarakteri:
        ekranaYaz("[!] OYUN SONLANDIRILDI")
        break
    elif "S" in islemKarakteri:
        Oyun().basla()
        break
    else:
        ekranaYaz("[x] Hatalı Giriş Yaptınız")
