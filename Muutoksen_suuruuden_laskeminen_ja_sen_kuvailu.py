#!/usr/bin/env python
# coding: utf-8

# # Muutoksen suuruuden laskeminen ja sen kuvailu Pythonin avulla

# ##### Muutoksen ja sen suuruuden kuvailussa käytetään yleensä
#  <UL>
#     <LI>tunnuslukuja monesta er näkökulmasta laskettuna</LI>
#     <LI>viivakuvioita</LI>
#     <LI>indeksejä ja niistä muodostettuja viivakuvioita</LI>
#     <LI>reaaliarvoja ja viivakuvioita</LI>
#     <LI>vertailua edelliseen vuoteen peräkkäisenä muutosprosenttina</LI>
#     <LI>vertailua edelliseen vuoteen pylväskuviona</LI>
#     </UL>
#         

# Käydään tässä läpi näitä kuvioita ja niihin liittyviä laskelmia. Datana on käytetty Tilastokeskuksen sivulta www.stat.fi (ks. Avainluvut-osio) haettuja vanhojen osakehuoneistojen hintoja kuukausittain pääkaupunkiseudulta ja muusta Suomesta viimeiseltä noin viideltä vuodelta. 

# Haettu data on tallennettu Haaga-Helian myy-palvelimen käyttäjätunnuksen rdi1lh101 hakemiston public_html alihakemistoon Dataa ja tiedoston nimi on Asuntojen_hinnat_viimeisin.xlsx. Siihen viitataan internet-protokollalla http://www.haaga-helia.fi/~rdi1lh101/Dataa/Asuntojen_hinnat_viimeisin.xlsx. Internet käyttäjät ohjataan siis automaattisesti käyttäjien public_html-hakemistoon, muut hakemistot ovat käyttäjän yksityisiä.

# Ensimmäisenä otetaan käyttöön Pythonin tarvittava perusohjelmakirjasto pandas, joiden avulla voidaan tehdä laskelmia.

# In[1]:


#### Ladataan pandas-kirjasto ja annetaan sille lempinimi pd

import pandas as pd


# Otetaan sitten datatiedosto käyttöön.

# In[2]:


##### Ladataan asuntojen hinnat sisältävä tiedosto ja annetaan sille nimi hinnat

hinnat = pd.read_excel('http://www.haaga-helia.fi/~rdi1lh101/Dataa/Asuntojen_hinnat_viimeisin.xlsx', sheet_name='Hinnat')

### Katsotaan, miltä sen kahdeksan ensimmäistä riviä näyttävät

hinnat.head(8)


# In[3]:


#### Tässä näkyvätkin sarakkeiden nimet. Ne voi myös tulostaa

hinnat.columns


# In[4]:


#### Muutetaan sarakkeiden nimet kirjoitusvirheille vähemmän alttiiksi mutta silti kuvaaviksi

hinnat.columns = ['Ajankohta', 'Pääkaupunkiseutu', 'Muu Suomi']

#### Ja tarkistetaan lopputulos

hinnat.columns


# In[5]:


#### Seuraavaksi Tilastokeskuksen datan päiväysmuotoilu pitää muuttaa ymmärrettäväksi.

#### Ensin riisutaan aineistossa oleva * pois luvun yhteydestä

hinnat['Ajankohta'] = hinnat['Ajankohta'].astype(str).str.strip('*')

#### Ladataan uusi kirjasto käyttöön kuukauden viimeisen päivän saamiseksi

from pandas.tseries.offsets import MonthEnd

#### Muutetaan Ajankohta-sarakkeen ilmaisu vastaavaksi kuukauden viimeiseksi päivämääräksi

hinnat['Ajankohta'] = pd.to_datetime(hinnat['Ajankohta'], format='%YM%m') + MonthEnd(0)

#### Katsotaan, miltä kahdeksan ensimmäistä riviä näyttää

#### Huomaathan, että indeksöinti alkaa nollasta. Näin aina.

hinnat.head(8)


# In[6]:


#### Lopuksi indeksöidään noiden päivämäärien mukaan

hinnat.set_index('Ajankohta')


# In[7]:


##### Tarkistetaan ensimmäiset kahdeksan riviä.
##### Huomaathan, että indeksöinti alkaa aina nollasta.

hinnat.head(8)


# In[8]:


##### Tarkistetaan viimeiset kuusi riviä

hinnat.tail(6)


# Lasketaan seuraavaksi tunnuslukuja näille luvuille.

# In[9]:


##### Tunnusluvut pääkaupunkiseudun ja muun Suomen vanhojen osakehuoneistojen vuosien 2015--2019 hinnoille

#### Huomaathan, että mediaani ilmaistaan 50 % prosenttipisteenä.

hinnat.describe()


# In[10]:


#### Yllä olevassa esitysmuodossa lukuja on hankala hahmottaa, kun desimaaleja on niin monta.

#### Lasketaan tunnusluvut kuten yllä, mutta esitetään tulokset kahdella desimaalilla

#### Kirjoitetaan luvut kahdella desimaalilla käyttäen style-muotoiluja.

hinnat.describe().style.format('{:.2f}')


# In[11]:


#### Tehdään näihin vielä yksi lisäys, otetaan lisäargumentilla useampia prosenttipisteet käyttöön

#### Seuraavassa käytetään 10 %, 25 %, 75 % ja 90 % prosenttipisteitä, muitakin voi lisätä samalla tavalla.

hinnat.describe(percentiles = [.1,.25,.75,.9]).style.format('{:.2f}')


# Tunnuslukuja voidaan laskea ja ryhmitellä eri tavoin. Lasketaan seuraavaksi vuosittaiset ja kuukausittaiset tunnusluvut kummallekin alueelle erikseen.

# In[12]:


##### Lasketaan hintojen tunnuslukuja pääkaunkiseudulle vuosittain

#### Kirjoitetaan luvut kahdella desimaalilla käyttäen style-muotoiluja.

hinnat.groupby(hinnat['Ajankohta'].dt.year)['Pääkaupunkiseutu'].describe(percentiles = [.1,.25,.75,.9]).style.format('{:.2f}')


# In[13]:


##### Lasketaan vastaavasti hintojen tunnuslukuja muulle Suomelle vuosittain

hinnat.groupby(hinnat['Ajankohta'].dt.year)['Muu Suomi'].describe(percentiles = [.1,.25,.75,.9]).style.format('{:.2f}')


# In[14]:


##### Lasketaan sitten hintojen tunnuslukuja kuukausittain
##### Ensin pääkaupunkiseutu

hinnat.groupby(hinnat['Ajankohta'].dt.month)['Pääkaupunkiseutu'].describe(percentiles = [.1,.25,.75,.9]).style.format('{:.2f}')


# In[15]:


##### Lasketaan sitten hintojen tunnuslukuja kuukausittain muualla Suomessa

hinnat.groupby(hinnat['Ajankohta'].dt.month)['Muu Suomi'].describe(percentiles = [.1,.25,.75,.9]).style.format('{:.2f}')


# Mitä vanhojen osakehuoneistojen neliöhinnoille on näiden laskelmien perusteella tapahtunut? Kuinka suuria muutokset ovat olleet ja mihin suuntaan ne ovat vaikuttaneet?

# Vaikuttaako myyntikuukausi näiden laskelmien perusteella neliöhintaan?
# Jos vaikuttaa, kuinka suuri vaikutus on?

# ### Lasketaan seuraavaksi indeksejä

# Indeksejä laskettaessa jokin ajankohta valitaan aluksi perusajankohdaksi. Muiden ajankohdan arvoja verrataan sitten perusajankohdan arvoon. Näiden arvojen suhdeluku kerrotaan sadalla.

# Valitaan tässä perusajankohdaksi vuoden 2015 tammikuu.

# In[17]:


#### Lisätään taulukkoon uudet sarakkeet indeksilukuja varten
#### Ensin pääkaupunkiseudun hintaindeksit

hinnat['PKS indeksi'] = hinnat['Pääkaupunkiseutu'] / hinnat['Pääkaupunkiseutu'].iloc[0] * 100


# In[18]:


##### Katsotaan, näyttävätkö laskelmat oikean suuntaisilta

hinnat.head()


# In[19]:


##### Katsotaan, näyttävätkö laskelmat oikean suuntaisilta

hinnat.tail()


# In[20]:


##### Tehdään sama muun Suomen hinnoille

#### Lisätään taulukkoon uusi sarake muun Suomen hintojen indeksilukuja varten

#### Listan ensimmäinen luku kiinnitetään argumentilla iloc[0].

hinnat['Muu Suomi indeksi'] = hinnat['Muu Suomi'] / hinnat['Muu Suomi'].iloc[0] * 100


# In[21]:


##### Katsotaan, näyttävätkö laskelmat oikean suuntaisilta

hinnat.head()


# In[22]:


##### Katsotaan, näyttävätkö laskelmat oikean suuntaisilta

hinnat.tail()


# Reaaliarvo laskettaessa yleinen hintojen muutoksen vaikutus poistetaan ja jäljellä jää todellinen, reaalinen, muutos.

# Tällaisissa tapauksissa lasketaan kaikkien arvojen reaaliarvo samana ajankohtana. Usein käytännön tilanteissa tuo on viimeisin tiedossa oleva ajankohta. Niin myös seuraavissa laskuissa eli vuoden 2019 syyskuu.

# Elinkustannusindeksi kuvaa yleisen hintatason muutoksia ja kahden ajankohdan elinkustannusindeksin suhde on kerroin, joka kertoo hintojen muutoksen suuruuden.

# Excel-tiedoston toisessa välilehdessä on asuntojen hintojen ajankohtien elinkustannusindeksit. Otetaan ne käyttöön ja lasketaan jokaiselle ajankohdalle kerroin, jolla sen ajankohdan hinta muutetaan vuoden 2019 syyskuun rahan arvoa vastaavaksi. 

# In[23]:


#### Luetaan elinkustannusindeksit Excel-tiedostosta tietokehykseen.

elinkustannusindeksi = pd.read_excel('http://www.haaga-helia.fi/~rdi1lh101/Dataa/Asuntojen_hinnat_2015-2019.xlsx', sheet_name='Elinkustannusindeksi')


# In[24]:


#### Katsotaan, miltä data näyttää alusta

elinkustannusindeksi.head()


# In[25]:


#### Katsotaan, miltä data näyttää lopusta

elinkustannusindeksi.tail()


# In[26]:


#### Ihan hyvältä näyttää, eikö.
#### Lisätään taulukkoon uusi sarake muutoskertoimia varten.
#### Tässä siis lasketaan kerroin, jolla muutetaan hinnat viimeisen kuukauden rahan arvoksi.

#### Listan viimeinen luku kiinnitetään argumentilla iloc[-1].

elinkustannusindeksi['Muutoskerroin'] = elinkustannusindeksi['Pisteluku'].iloc[-1] / elinkustannusindeksi['Pisteluku']


# In[27]:


#### Katsotaan lopputulosta alusta

elinkustannusindeksi.head()


# In[28]:


#### Ja lopusta

elinkustannusindeksi.tail()


# Näyttää järkevältä ja uskottavalta, eikö. Jatketaan siis.

# Lisätään tietokehykseen hinnat alkuperäisiä (nimellisiä) hintoja vastaavat reaaliarvoiset hinnat. Ne on siis laskettu viimeisen indeksin pisteluvun ajankohdan arvoa vastaaviksi.

# Jotta kunkin kuukauden neliöhinta löytää oikean kertoimella, jolla se kerrotaan viimeisen ajankohdan rahan arvoksi muutettaessa, tulee elinkustannusindeksi-tietokehyksessä ajankohdat muuttaa päivämääriksi samalla tavalla kuin yllä hinnat-tietokehyksessä.

# In[29]:


#### Muutetaan Tilastokeskuksen datan päiväysmuotoilu ymmärrettäväksi.

#### Ensin riisutaan aineistossa oleva * pois luvun yhteydestä

elinkustannusindeksi['Ajankohta'] = elinkustannusindeksi['Ajankohta'].astype(str).str.strip('*')

#### Muutetaan Ajankohta-sarakkeen ilmaisu vastaavaksi kuukauden viimeiseksi päivämääräksi

elinkustannusindeksi['Ajankohta'] = pd.to_datetime(elinkustannusindeksi['Ajankohta'], format='%YM%m') + MonthEnd(0)

#### Katsotaan, mitä tuli tehtyä. Kirjoitetaan siis kahdeksan ensimmäistä riviä näyttää

#### Huomaathan, että indeksöinti alkaa nollasta. Näin aina.

elinkustannusindeksi.head(8)


# In[30]:


#### Lopuksi indeksöidään noiden päivämäärien mukaan

elinkustannusindeksi.set_index('Ajankohta')


# In[31]:


##### Katsotaan taas, mitä onkaan tullut tehtyä.

elinkustannusindeksi


# In[32]:


##### Yhdistetään nyt hinnat-tietokehyksen Pääkaupunkiseudun ja Muun Suomen nimellishinnat sekä elinkustannusindeksi-tietokehyksen muutoskertoimet samaan tietokehykseen.
#### reaaliarvot = pd.concat([hinnat['Ajankohta'],elinkustannusindeksi['Ajankohta']], axis = 1)

reaaliarvot = pd.merge(hinnat, elinkustannusindeksi, how='left', on='Ajankohta')


# In[33]:


##### Miltähän näyttää?

reaaliarvot.head()


# In[34]:


##### Miltähän näyttää?

reaaliarvot.tail()


# Tässä on jo niin monta saraketta, että lukeminen vaikeutuu. Pidetään tässä tietokehyksessä vain reaaliarvojen laskemiseen liittyvät asiat ja poistetaan muut sarakkeet.

# In[35]:


##### Poistetaan indeksi-sarakkeet ja pisteluku-sarakkeet

reaaliarvot = reaaliarvot.drop(columns = ['PKS indeksi', 'Muu Suomi indeksi', 'Pisteluku'])


# Lisätään tähän sarakkeet Pääkaupunkiseudun ja Muun Suomen asuntojen reaaliarvoille ja lasketaan nuo reaaliarvot.

# In[36]:


##### Lasketaan ja lisätään reaaliarvot

reaaliarvot['PKS-reaali'] = reaaliarvot['Pääkaupunkiseutu'] * reaaliarvot['Muutoskerroin']

reaaliarvot['Muu-Suomi-reaali'] = reaaliarvot['Muu Suomi'] * reaaliarvot['Muutoskerroin']


# In[37]:


##### Katsotaan, miltä luvut näyttävät ja vaikuttavatko ne oikeilta.

reaaliarvot.head()


# In[38]:


##### Katsotaan, miltä luvut näyttävät ja vaikuttavatko ne oikeilta.

reaaliarvot.tail()


# In[39]:


##### TÄSSÄ TÄSSÄ TÄSSÄ


# ## Lasketaan muutosprosentteja

# Indeksejä laskettaessa verrattiin muutosta tiettyyn alussa kiinnitettyyn perusajankohdan arvoon. Toinen paljon käytetty tapa on verrata muutosta edelliseen arvoon. Esimerkkidatassa tämä tarkoittaa laskemista muutosta edellisen kuukauden hintaan nähden. Tämän voi tehdä nimellisillä tai reaalisilla arvoilla tai molemmilla. Tehdään nämä seuraavaksi.

# In[40]:


##### Lasketaan hintojen prosenttimuutokset aina edelliseen kuukauteen.

hinnat['PKS-muutos%'] = hinnat['Pääkaupunkiseutu'].pct_change()
hinnat['Muu-Suomi-muutos%'] = hinnat['Muu Suomi'].pct_change()


# In[41]:


##### Katsotaan laskujen tulosta ja tarkistetaan oikeellisuus

hinnat.head()


# In[42]:


#### Muutetaan prosenttimuotoilut desimaaliesityksestä prosenttiluvuiksi


#### hinnat.style.format({'PKS-muutos%': '{:.2f} %'})

#### hinnat.style.format({'Muu-Suomi-muutos%': '{:.2f} %'})


# In[43]:


##### Katsotaan laskujen tulosta ja tarkistetaan oikeellisuus

hinnat.tail()

##### .style.format({'PKS-Muutos%': '{:.1f} %'})


# In[44]:


##### Yhdistetään pääkaupunkiseudun ja muun Suomen hintojen muutokset omaan tietokehykseen

muutokset = pd.concat([hinnat['PKS-muutos%'],hinnat['Muu-Suomi-muutos%']], axis =1)


# In[45]:


#### Katsellaan, miltä näyttää

muutokset.head(10)


# In[46]:


#### Katsellaan, miltä näyttää

muutokset.tail(10)


# ## Kuviot

# Lopuksi piirretään kuvioita äsken lasketuista asioista. Aluksi tarvitaan jälleen apua Pythonin kirjastoista, joiden avulla kuviot saadaan tehtyä. Otetaan ne käyttöön.

# In[47]:


#### Käytetään kirjastoa matplotlib ja annetaan sille lempinimi plt.

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use('seaborn-whitegrid')


# Piirretään ensin viivakuvio alkuperäisistä pääkaupunkiseudun ja muun Suomen neliöhinnoista. Parannellaan kuvaa vähitellen, jotta eri osien merkitys valkenee.

# In[48]:


##### Piirretään pääkaupunkiseudun neliöhinnoista viivakuvio.

#### Viivakuvio on oletusarvo eikä sitä tarvitse erikseen kuviotyyppinä mainita.

hinnat['Pääkaupunkiseutu'].plot()


# In[49]:


##### Samalla tavalla piirretään muun Suomen neliöhinnoista viivakuvio.

hinnat['Muu Suomi'].plot()


# In[50]:


#### Entä kummatkin yhteen kuvioon. yhteen

hinnat['Pääkaupunkiseutu'].plot()
hinnat['Muu Suomi'].plot()


# Laitetaan pääkaupunkiseudun asuntojen hintakuvio kuntoon.

# In[51]:


##### Luodaan figure- ja axes-oliot

fig1, ax1 = plt.subplots(figsize=(10,6))

##### Määritetään ax1-olio:

color = 'C0'
ax1.set(ylabel = 'Neliöhinta', xlabel = 'Päivämäärä', title = 'Pääkaupunkiseutujen asuntojen hinnat')

ax1.plot(hinnat['Pääkaupunkiseutu'], color=color)


# In[52]:


##### Jos tähän halutaan muun Suomen hinnat mukaan, lisätään ne samaan kuvaan

##### Luodaan figure- ja axes-oliot

fig1, ax1 = plt.subplots(figsize=(10,6))

##### Määritetään ax1-olio:

color = 'C0'
ax1.set(ylabel = 'Neliöhinta', xlabel = 'Päivämäärä', title = 'Pääkaupunkiseutujen asuntojen hinnat')

ax1.plot(hinnat['Pääkaupunkiseutu'], color=color)

ax1.plot(hinnat['Muu Suomi'], color=color)


# In[53]:


#### Hankalampi tapaus on sellainen, jossa kummallekin tarvitaan oma pystyakseli. 

##### Luodaan toinen axes-olio, jolla on yhteinen x-akseli ax1-olion kanssa:

ax2 = ax1.twinx()

color = 'C1'
ax2.set_ylabel('Muun Suomen hinnat', color=color)
ax2.plot(hinnat['Muu Suomi'], color=color)
ax2.tick_params(axis='y', labelcolor=color, grid_color=color)


# In[54]:


##### Lopuksi yhdistetään nämä kaksi.

##### Luodaan figure- ja axes-oliot

fig1, ax1 = plt.subplots(figsize=(10,6))

##### Määritetään ax1-olio:

color = 'C0'
ax1.set(ylabel = 'Pääkaupunkiseudun neliöhinta', xlabel = 'Päivämäärä', title = 'Pääkaupunkiseuden ja muun Suomen asuntojen hinnat')

ax1.plot(hinnat['Pääkaupunkiseutu'], color=color)

##### Luodaan toinen axes-olio, jolla on yhteinen x-akseli ax1-olion kanssa:

ax2 = ax1.twinx()

color = 'C1'
ax2.set_ylabel('Muun Suomen neliöhinta', color=color)
ax2.plot(hinnat['Muu Suomi'], color=color)
ax2.tick_params(axis='y', labelcolor=color, grid_color=color)


# ### Piirretään reaaliarvoja

# Piirretään reaaliarvoista vastaava kuvaaja.

# In[55]:


##### Piirretään reaaliarvot samaan kuvaan.

##### Luodaan figure- ja axes-oliot

fig_real, ax_real = plt.subplots(figsize=(10,6))

##### Määritetään ax-olio:

ax_real.set(ylabel = 'Neliön reaalihinta', xlabel = 'Päivämäärä', title = 'Asuntojen reaalihintojen muutokset')

ax_real.plot(reaaliarvot['PKS-reaali'], color='red', label = 'Pääkaupunkiseutu')

ax_real.plot(reaaliarvot['Muu-Suomi-reaali'], color='purple', label ='Muu Suomi', linestyle='dashed')

#### legend = True  ### ei toimi


# In[56]:


##### Piirretään nämä vielä samaan kuvioon.

##### Luodaan figure- ja axes-oliot

##### Tässä oli onglemia: subplotilla ei ollut coloria, linestyleä yms.

fig_real1, ax_real1 = plt.subplots(figsize=(10,6))

##### Määritetään ax1-olio:

color = 'C0'
ax_real1.set(ylabel = 'Pääkaupunkiseudun reaalihinta neliöltä', xlabel = 'Päivämäärä', title = 'Pääkaupunkiseuden ja muun Suomen asuntojen reaalihinnat')

ax_real1.plot(reaaliarvot['PKS-reaali'], label='Pääkaupunkiseudun reaalihinnat')

##### Luodaan toinen axes-olio, jolla on yhteinen x-akseli edellisen olion kanssa:

ax_real2 = ax_real1.twinx()

color = 'C1'
ax_real2.set(ylabel='Muun Suomen reaalihinta neliöltä', label='Muun Suomen reaalihinnat')
ax_real2.plot(reaaliarvot['Muu-Suomi-reaali'])
### ax_real2.tick_params(axis='y', labelcolor=color, grid_color=color)


# ### Piirretään indeksejä

# Indekseillä kuvataan hintojen muutoksien suuruuksia ja suuntia. Niitä kuvataan tavallisesti viivakuviolla.

# In[57]:


##### Piirretään indeksit samaan kuvaan.

##### Luodaan figure- ja axes-oliot

fig_index, ax_index = plt.subplots(figsize=(10,6))

##### Määritetään ax1-olio:


ax_index.set(ylabel = 'Indeksin pisteluku', xlabel = 'Päivämäärä', title = 'Asuntojen hintojen muutokset')

ax_index.plot(hinnat['PKS indeksi'], color='blue', label = 'Pääkaupunkiseutu')

ax_index.plot(hinnat['Muu Suomi indeksi'], color='green', label ='Muu Suomi', linestyle='dashed')

#### legend = True  ### ei toimi


# Tarkastele ensin alkuperäisistä arvoista tehtyä viivakuviota. Näyttääkö sinusta siltä, että toinen arvoista muuttuu toista nopeammin? Entä jos vertaat samaa asiaa indekseistä? Mitä johtopätöksiä voit tehdä?

# ### Piirretään peräkkäisiä muutosprosentteja

# Indeksien yhteydesä huomattiin, että siellä jokaista muutosta verrattiin aina yhteen lukuun, esim. ensimmäiseen hintatietoon. 

# Toinen tapa on verrata muutosta edelliseen vuoteen. Edellä laskettiin aineistosta prosenttimuutoksia edellisen vuoden neliöhintoihin pääkaupunkiseudun ja muun Suomen asunnoista. Näitä kuvataan pylväskuviolla.Tehdään seuraavaksi vielä tälläinen kuvio.

# In[58]:


##### Tehdään viimeisen kymmenen arvon muutoksista pylväskaavio

##### Kuviotyyppi pitää nyt kertoa. 
##### Viimeiset kymmenen ja vaaka-akselin teksti 45 asteen kulmassa

ax_pera = muutokset[-10:].plot.bar(rot=45)

##### Pystyakselin otsikko

ax_pera.set_ylabel('Muutosprosentti edelliseen päivään')

##### Kuvion otsikko

ax_pera.set_title('Pääkaupunkiseudun ja muun Suomen asuntojen neliöhintojen päivämuutokset')

##### Vaaka-akselin otsikko

ax_pera.set_xlabel('Tarkasteluaika')


# Käy läpi kymmenen viime havainnon kohdalta, milloin pääkaupunkisuedun ja muun Suomen neliöhinnat ovat nousseet ja milloin taas laskeneet. Mieti, miten se kuviossa näkyy. Erityisesti, kommentoi ovatko komanneksi viimeisen havainnon kohdalla muun Suomen neliöhinnat korkeammat vai alemmat kuin edellisen vuoden neliöhinnat.
