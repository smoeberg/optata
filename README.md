# Optata

Verificeret efterspørgsel på boligmarkedet: købere registrerer, hvad de vil købe, og ejere kan logge ind og se interessen for deres område, gade og hus.

## Indhold

| Sti | Indhold |
|---|---|
| `docs/Optata - Projektgrundlag v5.1.md` | Masterdokumentet: forretning, koncept, data, mekanismer, sikkerhed, jura og leveranceplan |
| `docs/historik/Optata - Projektgrundlag v5.0.md` | Forrige version |

Ændringerne fra v5.0 til v5.1 står i §0.2 i masterdokumentet. De åbne beslutninger står i §0.3.

## Mangler i repoet

Disse filer er nævnt i masterdokumentets bilag B, men er endnu ikke lagt ind:

- Optata - Forretningsplan v4.2.md
- Optata - Arkitekturreview v4.2.md
- Optata - Finansiel Model 36 Mdr.xlsx
- De elleve tekniske bilag (`attachments/altf73/*.txt`)

## Regler for koden

Kode er endnu ikke påbegyndt. Når den kommer, gælder reglerne i masterdokumentets §7:

- Udvikling sker kun på syntetiske data. Ingen persondata i repoet.
- Guards, RLS, vault, reveal, finansiel logik og sletning skrives og godkendes af et menneske.
- En rød guard-test blokerer merge.
