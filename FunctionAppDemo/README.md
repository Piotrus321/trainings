1. Opis aplikacji:
HttpParserApp - działa w oparciu o HTTP request, po jego otrzymaniu wraz z nazwą pliku w body requestu parsuje excelka do csvki
BlobTriggerParser - skanuje dany blob kontener i parsuje każdy plik, który do niego trafi zostaje przeniesony do CSV, bez użycia dodatkowych bibliotek, tylko funkcjonalość obecna w ramach azure.functions
TimerTriggerDelta - skanuje dany blob container i co określony czas (2 min) transformuje wszystkie pliki do Delty

2. Opis struktury folderu:
.venv - wirtualne środowiska Pythona, nie jest wrzucane do repozytorium i należy je odtworzyć po sklowaniu kodu https://realpython.com/python-virtual-environments-a-primer/
.vscode - pliki konfiguracyjne VSCoda, konieczne do lokalnego debugowania apek
.funcignore - opisuje pliki, które mają nie zostać zdeplyowane do Azure
.gitignore - pliki, które nie mają zostać przeniesione do Gita
host.json - plik z dodatkowymi konfiguracjami całej Function Apki
__init__.py - kod źródłowej każdej funkcji
function.json - plik konfiguracyjny każdej pojedynczej funkcji, opisuje triggery, input i output bindingi
local.settings.json - lokalne App settingi, tutaj proponowane jest umieszczać wszystkie zmienne środowiskowe które nie powinny być hardcodowane
mappings.json - zewnętrzny plik z mappingami do parsowania excela, do umieszczania app settingsach Function Appy
requirments.txt - opisuje biblioteki do ściągnięcia

3. Wymagania autoryzacyjne:
HttpParserApp - Storage Blob Data Contributor, żeby odczytać,zapisać i usunąć plik z bloba
BlobTriggerParser -  Storage Blob Data Owner (możliwe że Contributor wystarczy), Storage Queue Data Contributor
TimerTriggerDelta - Key Vault Secrets User

4. Komentarze
local.settingsy dla treningowej referencji, Connection stringi nigdy nie powinny zostać umieszoncze w Repo :D

5. Niezbędne do developowania:
-VSCode + Azure Functions/Azure Account/Azurite/Python extensions (coś do testowania API też byłoby spoko jak Thunder Client/Postman extension w VsCodzie) 
-Python w wersji 3.7 do 3.10 (3.10 najlepiej raczej) 
-.Net https://dotnet.microsoft.com/en-us/download
-Azure Functions Core tools https://go.microsoft.com/fwlink/?linkid=2174087
