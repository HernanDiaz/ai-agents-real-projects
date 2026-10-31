<!-- Encabezado en HTML: GitHub Pages no interpreta Markdown dentro de un <div>, y así se ve igual en los dos sitios. -->
<div align="center">
  <h1>Agentes II: trabajar con agentes en proyectos reales</h1>
  <h3><em>El banco de trabajo de un agente de programación: instrucciones, contratos, verificación y revisión, con modelos abiertos en Python</em></h3>
  <p>por <strong>Hernán Díaz Rodríguez, PhD</strong> · Profesor en la Universidad de Oviedo</p>
  <p>
    <a href="https://creativecommons.org/licenses/by-nc/4.0/deed.es"><img src="https://img.shields.io/badge/Licencia-CC%20BY--NC%204.0-lightgrey.svg" alt="Licencia: CC BY-NC 4.0"></a>
    <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Colab-GPU%20T4%20gratuita-orange?logo=googlecolab" alt="Colab">
  </p>
</div>

---

## El libro

**Agentes II** da el salto del agente de un solo archivo a un repositorio de verdad: el programa de gestión de **Ciclos Norte**, una tienda de bicicletas de Oviedo, con varios módulos, pruebas y una lista de tareas como la de un equipo real. Ahí el agente falla mucho, y casi nunca porque el modelo sea malo: le falta saber qué puede tocar, cómo comprobar que ha terminado, qué pasó en la sesión anterior y quién revisa lo que hace. A todo eso lo llamamos el **banco de trabajo**, y cada capítulo añade una pieza y la mide: instrucciones que se pueden comprobar, el estado entre sesiones, contratos de alcance, retroalimentación y puertas de verificación, un revisor con rúbrica, entender antes de cambiar, delegar con aislamiento, especificaciones, métricas de éxito y permisos y límites. El último capítulo instala el banco completo en un repositorio que el agente no ha visto nunca, el de una clínica veterinaria.

Lo que se mide no es solo cuántas tareas resuelve el agente, sino cuánto vale su palabra «terminado», cuántas reglas rompe, cuántas tareas escala con una explicación en lugar de esconderlas y cuánto tiempo de persona cuesta. Todo se programa en Python con **modelos abiertos y gratuitos**, sin claves de API ni servicios de pago: Qwen3-4B-Instruct-2507 en la GPU gratuita de Colab. Las tareas se comprueban con pruebas ocultas que el agente no ve, y cada cifra del libro sale de un experimento que puedes repetir en el cuaderno del capítulo.

Forma parte de la colección **IA en práctica**: libros prácticos de inteligencia artificial con experimentos propios, un cuaderno y un vídeo en cada capítulo.

---

## Capítulos

Cada capítulo tiene su cuaderno en Google Colab y su vídeo, con Robotín y el autor. Todos los vídeos están en la [lista de reproducción de YouTube](https://www.youtube.com/playlist?list=PLCSg5CpcZnMg).

| Cap. | Título | Cuaderno | Vídeo |
|------|--------|----------|-------|
| 1 | Por qué fallan los agentes: el banco de trabajo | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/cuadernos/1_Por_que_fallan_los_agentes.ipynb) | [![Ver en YouTube](https://img.shields.io/badge/YouTube-Ver%20v%C3%ADdeo-red?logo=youtube)](https://www.youtube.com/watch?v=SAIuvY2aoIU&list=PLCSg5CpcZnMg) |
| 2 | Instrucciones que se pueden comprobar | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/cuadernos/2_Instrucciones_que_se_pueden_comprobar.ipynb) | [![Ver en YouTube](https://img.shields.io/badge/YouTube-Ver%20v%C3%ADdeo-red?logo=youtube)](https://www.youtube.com/watch?v=Rzn1qohDrEc&list=PLCSg5CpcZnMg) |
| 3 | Memoria del repositorio e inicialización | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/cuadernos/3_Memoria_del_repositorio.ipynb) | [![Ver en YouTube](https://img.shields.io/badge/YouTube-Ver%20v%C3%ADdeo-red?logo=youtube)](https://www.youtube.com/watch?v=UFH746Iw-_A&list=PLCSg5CpcZnMg) |
| 4 | Contratos de alcance | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/cuadernos/4_Contratos_de_alcance.ipynb) | [![Ver en YouTube](https://img.shields.io/badge/YouTube-Ver%20v%C3%ADdeo-red?logo=youtube)](https://www.youtube.com/watch?v=1ToQwkPI4I4&list=PLCSg5CpcZnMg) |
| 5 | Retroalimentación y puertas de verificación | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/cuadernos/5_Retroalimentacion_y_verificacion.ipynb) | [![Ver en YouTube](https://img.shields.io/badge/YouTube-Ver%20v%C3%ADdeo-red?logo=youtube)](https://www.youtube.com/watch?v=NOXsTN4H3CM&list=PLCSg5CpcZnMg) |
| 6 | El revisor | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/cuadernos/6_El_revisor.ipynb) | [![Ver en YouTube](https://img.shields.io/badge/YouTube-Ver%20v%C3%ADdeo-red?logo=youtube)](https://www.youtube.com/watch?v=UXpQPFuLaTg&list=PLCSg5CpcZnMg) |
| 7 | Entender antes de cambiar | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/cuadernos/7_Entender_antes_de_cambiar.ipynb) | [![Ver en YouTube](https://img.shields.io/badge/YouTube-Ver%20v%C3%ADdeo-red?logo=youtube)](https://www.youtube.com/watch?v=hSO7JdNpsfQ&list=PLCSg5CpcZnMg) |
| 8 | Delegar con aislamiento | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/cuadernos/8_Delegar_con_aislamiento.ipynb) | [![Ver en YouTube](https://img.shields.io/badge/YouTube-Ver%20v%C3%ADdeo-red?logo=youtube)](https://www.youtube.com/watch?v=wSCBiENXQMo&list=PLCSg5CpcZnMg) |
| 9 | Del flujo real a la especificación | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/cuadernos/9_Del_flujo_real_a_la_especificacion.ipynb) | [![Ver en YouTube](https://img.shields.io/badge/YouTube-Ver%20v%C3%ADdeo-red?logo=youtube)](https://www.youtube.com/watch?v=FyFNbD7IkMc&list=PLCSg5CpcZnMg) |
| 10 | Métricas de éxito | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/cuadernos/10_Metricas_de_exito.ipynb) | [![Ver en YouTube](https://img.shields.io/badge/YouTube-Ver%20v%C3%ADdeo-red?logo=youtube)](https://www.youtube.com/watch?v=YsDMjix4UK0&list=PLCSg5CpcZnMg) |
| 11 | Permisos, puntos de control y límites de coste | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/cuadernos/11_Permisos_y_limites.ipynb) | [![Ver en YouTube](https://img.shields.io/badge/YouTube-Ver%20v%C3%ADdeo-red?logo=youtube)](https://www.youtube.com/watch?v=vrGjbTD8Ygk&list=PLCSg5CpcZnMg) |
| 12 | Proyecto: un banco de trabajo para un repositorio real | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/cuadernos/12_Banco_de_trabajo.ipynb) | [![Ver en YouTube](https://img.shields.io/badge/YouTube-Ver%20v%C3%ADdeo-red?logo=youtube)](https://www.youtube.com/watch?v=Ct3Deebry10&list=PLCSg5CpcZnMg) |

---

## Cómo usar los cuadernos

- Pulsa **Abrir en Colab** y ejecuta las celdas en orden. La primera celda instala las versiones de las bibliotecas con las que se comprobó el libro.
- Activa la GPU gratuita: *Entorno de ejecución → Cambiar tipo de entorno de ejecución → GPU T4*. El modelo ocupa unos 8 GB y la primera vez tarda unos minutos en descargarse. El capítulo 10 y muchas secciones de los demás no necesitan GPU.
- Los cuadernos descargan solos, la primera vez, las carpetas `datos/` y `comun_libro/` de este repositorio.
- Ejecutar un experimento completo lleva horas; los cuadernos traen ejemplos cortos, y los resultados completos que cita el libro están guardados en `datos/resultados/`, así que casi todos los ejercicios se hacen sin GPU. Las cifras pueden variar un poco con otra GPU u otras versiones de las bibliotecas.

---

## Estructura del repositorio

```
ai-agents-real-projects/
├── cuadernos/         ← Un cuaderno por capítulo
├── comun_libro/       ← Las herramientas del agente: leer, buscar, editar, ejecutar las pruebas
├── datos/
│   ├── ciclos_norte/      ← El repositorio de la tienda en el que trabaja el agente
│   ├── tareas/            ← Las tareas T01 a T35, con sus pruebas ocultas y su solución
│   ├── clinica_naranco/   ← El repositorio de la clínica veterinaria (capítulo 12)
│   ├── incidencias/       ← Las incidencias I01 a I08 de la clínica
│   └── resultados/        ← Los resultados de los experimentos del libro
└── cuaderno/N/        ← Los enlaces del libro a cada cuaderno en Colab
```

---

## Datos

Ciclos Norte, la Clínica Veterinaria Naranco y todos sus datos son inventados. El agente trabaja siempre sobre una copia del repositorio que se crea para cada tarea, así que puedes equivocarte sin consecuencias.

| Carpeta | Contenido | Capítulos |
|---------|-----------|-----------|
| `ciclos_norte/` | El programa de gestión de la tienda: pedidos, envíos, devoluciones, existencias, presupuestos, facturas, avisos e informes, con sus pruebas | 1 a 11 |
| `tareas/` | 35 tareas (fallos, funciones nuevas, cambios de reglas y refactorizaciones), cada una con su petición, su contrato, sus pruebas ocultas y una solución de referencia | 1 a 9 |
| `clinica_naranco/` | El programa de gestión de una clínica veterinaria: citas, vacunas, farmacia, facturas y avisos | 12 |
| `incidencias/` | Ocho incidencias de la clínica, escritas por quien las sufre, con su contrato y sus pruebas ocultas | 12 |
| `resultados/` | Las ejecuciones del libro, con cada intento del agente; los capítulos 10 y 11 las analizan sin volver a ejecutar nada | 7 a 12 y ejercicios |

---

## El autor

**Hernán Díaz Rodríguez** es profesor del Departamento de Ciencias de la Computación e Inteligencia Artificial de la **Universidad de Oviedo**, donde se doctoró en Informática. Trabajó cinco años como ingeniero de software en el **CERN**.

[LinkedIn](https://www.linkedin.com/in/hernandiazrodriguez) · [Correo](mailto:hernan.diaz.rodriguez@gmail.com) · [Página de autor en Amazon](https://www.amazon.es/Hernan-Diaz-Rodriguez/e/B0GD8JQ9JB)

---

## Licencia

Este material se distribuye bajo la licencia [Creative Commons Reconocimiento-NoComercial 4.0 Internacional (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/deed.es): se puede usar y adaptar para docencia y estudio citando al autor, pero no con fines comerciales.

El modelo que usan los cuadernos, Qwen3-4B-Instruct-2507, se distribuye con licencia Apache 2.0.

## Cómo citar

```bibtex
@book{diazrodriguez2026agentesii,
  author    = {Hern{\'a}n D{\'\i}az Rodr{\'\i}guez},
  title     = {Agentes II: trabajar con agentes en proyectos reales. El banco de trabajo de un agente de programaci{\'o}n: instrucciones, contratos, verificaci{\'o}n y revisi{\'o}n, con modelos abiertos en Python},
  year      = {2026},
  publisher = {Publicaci{\'o}n independiente},
  url       = {https://github.com/HernanDiaz/ai-agents-real-projects}
}
```
