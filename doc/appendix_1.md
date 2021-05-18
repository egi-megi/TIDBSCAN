## Appendix 1
Do pierwszej części raportu użyto następujących danych:

|Nr|Konto|Plik|
|:-:|:-:|:-:|
|1|@BarackObama|[BarackObama.csv](../data/BarackObama.csv)|
|2|@BillGates|[BillGates.csv](../data/BillGates.csv)|
|3|@BorisJohnson|[BorisJohnson.csv](../data/BorisJohnson.csv)|
|4|@elonmusk|[elonmusk.csv](../data/elonmusk.csv)|
|5|@jk_rowling|[jk_rowling.csv](../data/jk_rowling.csv)|
|6|@KamalaHarris|[KamalaHarris.csv](../data/KamalaHarris.csv)|
|7|@PolandMFA|[PolandMFA.csv](../data/PolandMFA.csv)|
|8|@Pontifex|[Pontifex.csv](../data/Pontifex.csv)|
|9|@POTUS|[POTUS.csv](../data/POTUS.csv)|
|10|@RobertDowneyJr|[RobertDowneyJr.csv](../data/RobertDowneyJr.csv)|
|11|@RoyalFamily|[RoyalFamily.csv](../data/RoyalFamily.csv)|

Data dostępu do danych: 01.05.2021

Dane zostały zczytane narzędziem [AllMyTweets](https://www.allmytweets.net/) oraz pobrane do pliku `.csv` wtyczką do Google Chrome - [Instant Data Scraper](https://chrome.google.com/webstore/detail/instant-data-scraper/ofaokhiedipichpaobibbnahnkdoiiah). Jak widać w przykładowej linijce `.csv` cały tekst zawarty jest w pierwszej kolumnie a w kolejnych zawarte są inne informacje jak link do tweetu czy linki do zawartości www:
|tablescraper-selected-row|tablescraper-selected-row href|grey|linkified|linkified href|
|-|-|-|-|-|
|"Time to head #Downstream....@fp_coalition ""Downstream Channel"" is an exploration and discussion of environmental issues and challenges, featuring interviews with fascinating guests. 🌎🙏🎙Out NOW, only on YouTube -"|https://twitter.com/RobertDowneyJr/status/1387826384983179264|"Apr 29, 2021"|https://t.co/cqTRp60Qo3|http://t.co/cqTRp60Qo3|


Metodą [`read_n_tweets_from_data(path=, number=)`](../tweets.py#L28) wczytujemy zdania tweetów z plików csv. Jedyna logika zaprzęgnięta to pomijanie pustych tweetów (może się zdarzyć w przypadku tweetowania samych linków). Ta metoda zwraca wektor wczytanych tweetów oraz odpowiadający mu wektor z klasą przynależności tweeta. W przypadku naszej analizy, pobieraliśmy po `number=50` tweetów od każdego z wymienionych wyżej użytkowników.

Następnym krokiem jest użycie metody [`get_vectors(tweets_list)`](../tweets.py#L50) która opakowuje wywołanie zewnętrznej biblioteki zamieniającej wektor tekstu na wektor liczbowy.

Na tym kończy się wczytywanie i użycie danych. Użycie oraz wyniki opisane w raporcie można zreprodukować w tym [notebooku](../tweets.ipynb).