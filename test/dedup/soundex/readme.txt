Test:  Soundex deduplication
Created by:  Karen Fishwick


Input file structure:
BIRTH_DATE,PREF_FIRST_GIVEN_NAME,PREF_FAMILY_NAME,COMMUNITY_OR_LOCATION,CANADIAN_POSTAL_CODE,INGESTION_ID


Dedup project :
Block match on birth date, pref family name, community, and postal code, soundex max edits 2 on pref first given name

Test cases:

1.  Soundex should match
19890827,GRACIE0,SANTIAGO,RICHMOND,V6X4H7, 1
19890827,GRACIE,SANTIAGO,RICHMOND,V6X4H7,2

2.  Soundex should match the first two, but not the third
19790813,ARCHER,SCIBELLI,KASLO,V0G1M0,3
19790813,ARGUER,SCIBELLI,KASLO,V0G1M0,4
19790813,APTER,SCIBELLI,KASLO,V0G1M0,5

3.  Soundex should match all three
19210721,DAGGAL,SZOCINSKI,VANDERHOOF,V0J3A0,6
19210721,DOUGAL,SZOCINSKI,VANDERHOOF,V0J3A0,7
19210721,DOUGHILL,SZOCINSKI,VANDERHOOF,V0J3A0,8


