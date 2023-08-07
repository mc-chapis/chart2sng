# chart2sng
conversor de .chart (FeedBack/Moonscraper) pra .sng (Freetar Editor/Guitar Flash)

## Como usar
1. Instale o Python 3 através da Microsoft Store;
2. Baixe e abra o arquivo `chart2sng.py` (se ele não abrir com duplo-clique, tente utilizar o botão direito > Abrir com... > Python 3.x)
3. Siga as instruções durante a execução do arquivo.

### O programa não está funcionando corretamente
Verifique que a chart tem os parâmetros `Name`, `Artist` e `MusicStream`. Exemplo:
```Ini
[Song]
{
  Name = "Nome da música"
  Artist = "Artista"
  Offset = -5.5
  Resolution = 480
  Player2 = bass
  Difficulty = 0
  PreviewStart = 0
  PreviewEnd = 0
  Genre = "rock"
  MediaType = "cd"
  MusicStream = "C:\pasta\da\musica\song.mp3"
}
```
### A chart está atrasada/adiantada em relação ao vídeo do YouTube
Uma forma de consertar é alterando o parâmetro `Syncrony` na própria plataforma de customs do Guitar Flash.

**Porém**, o conversor suporta o parâmetro `Offset` na chart (em segundos, demonstrado no exemplo acima, as notas da chart serão empurradas 5.5 segundos pra trás após a conversão).
