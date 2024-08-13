Claro! Aqui está uma versão aprimorada do README, incluindo a funcionalidade de demonstração usando a webcam:

---

# README

## Visão Geral

Este repositório contém scripts para comparar movimentos corporais entre dois vídeos ou diretamente usando a webcam, utilizando o modelo de detecção de pose do MediaPipe. O objetivo principal é medir a similaridade entre as poses detectadas nos vídeos de referência e usuário, fornecendo feedback visual sobre a precisão dos movimentos.

## Estrutura do Projeto

### Arquivos

- `CompararMovimentos.py`: Script para comparar movimentos entre dois vídeos ou usar a webcam para comparação em tempo real e exibir a precisão dos movimentos.
- `DetrectorPoses.py`: Contém a classe `DetectorPoses` que utiliza o MediaPipe para detectar e analisar poses corporais em vídeos.

## Dependências

Antes de executar os scripts, você precisa instalar as seguintes bibliotecas:

- `opencv-python`
- `mediapipe`
- `scipy`
- `fastdtw`

Você pode instalar essas dependências usando `pip`:

```bash
pip install opencv-python mediapipe scipy fastdtw
```

## `CompararMovimentos.py`

Este script permite comparar o movimento corporal detectado em dois vídeos (um de referência e um do usuário) ou diretamente usando a webcam, fornecendo feedback sobre a precisão dos movimentos em tempo real.

### Funcionalidades

- **Leitura de Vídeos ou Webcam**: Carrega dois vídeos ou usa a webcam para captura ao vivo.
- **Detecção de Pose**: Utiliza a classe `DetectorPoses` para detectar poses nos vídeos ou na captura ao vivo.
- **Comparação de Movimentos**: Calcula a similaridade entre as poses usando a distância de cosseno e o algoritmo FastDTW.
- **Exibição de Resultados**: Mostra o erro de similaridade, se o movimento é correto ou incorreto, e a precisão dos passos executados.

### Como Executar

1. **Para comparação com vídeos**:

    Certifique-se de que os vídeos estejam acessíveis no caminho fornecido e execute o script:

    ```bash
    python CompararMovimentos.py
    ```

    Certifique-se de substituir `ref_video` e `user_video` pelos caminhos dos seus vídeos.

2. **Para comparação com a webcam**:

    Se desejar testar com a webcam, ajuste o script para usar as feeds da webcam como entrada. O código atual pode ser modificado para capturar vídeo diretamente da webcam.

### Parâmetros

- `ref_video`: Caminho para o vídeo de referência.
- `user_video`: Caminho para o vídeo do usuário.

## `DetrectorPoses.py`

Este script define a classe `DetectorPoses`, que é responsável pela detecção e análise de poses corporais em vídeos.

### Funcionalidades

- **Detecção de Pose**: Detecta landmarks corporais em imagens de vídeo.
- **Identificação de Posições**: Obtém a lista de coordenadas dos landmarks detectados.
- **Cálculo de Ângulos**: Calcula ângulos entre pontos específicos do corpo.

### Métodos

- `__init__(self, mode=False, cimaCorpo=False, suavizacao=True, detecContorno=0.7, trackCon=0.7)`: Inicializa o detector com configurações personalizáveis.
- `identificarPose(self, img, draw=True)`: Processa a imagem para detectar poses e opcionalmente desenhar landmarks e conexões.
- `identificarPosicao(self, img, draw=True)`: Obtém a lista de posições dos landmarks e opcionalmente desenha os pontos na imagem.
- `encontrarAngulo(self, img, p1, p2, p3, draw=True)`: Calcula o ângulo entre três pontos específicos do corpo e opcionalmente desenha o ângulo na imagem.

### Como Executar

Para testar o `DetectorPoses`, você pode executar o script diretamente:

```bash
python DetrectorPoses.py
```

Certifique-se de que o vídeo especificado na linha `cap = cv2.VideoCapture(r'Video_teste/bulgaro_teste.mp4')` está acessível.

## Observações
O projeto foi testado no Ubuntu. As dependências estão listadas no requirements.txt.

## Demonstração
Veja o vídeo de demonstração do projeto aqui.
<video src="https://github.com/belokelvin/ComparadorDePoses/blob/main/Video_teste/Teste_demo.mp4" width="320" height="240" controls></video>

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para fazer pull requests ou abrir issues.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

Sinta-se à vontade para ajustar qualquer parte do README conforme necessário!
