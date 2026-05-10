QUERIES PROFESIONALES 

Las queries deben ser:

Transversales (multi-documento).

Analíticas (no solo extracción).

Orientadas a la ejecución de obra.

BLOQUE 1 — DETECCIÓN DE INCIDENCIAS

1\.	¿Cuáles son las incidencias más frecuentes en todas las actas?



2\.	¿Qué tipos de problemas aparecen con mayor recurrencia en las obras?



3\.	Agrupa todas las incidencias detectadas en las actas y clasifícalas por tipo:

a.	estructural

b.	seguridad

c.	ejecución

d.	instalaciones



4\.	Identifica todas las frases que describen problemas o patologías en la infraestructura.



5\.	Lista todas las afecciones detectadas en andenes, estructuras o instalaciones.



BLOQUE 2 - RIESGO GLOBAL DE PROYECTOS

6\.	¿Qué obras presentan mayor riesgo en función de las incidencias detectadas?



7\.	Identifica patrones de riesgo recurrentes en las actas



8\.	¿Qué problemas pueden afectar a la seguridad de la explotación ferroviaria?



Ejemplo real:

“riesgo de afección a la circulación”  



BLOQUE 3 – ANÁLISIS DE TENDENCIAS

9\.	¿Cómo evolucionan las incidencias a lo largo del tiempo?



10\.	¿Se repiten los mismos problemas en diferentes fases de obra?





11\.	Detecta tendencias en retrasos o problemas técnicos.

BLOQUE 4 - ELEMENTOS MÁS PROBLEMÁTICOS

12\.	¿Qué elementos constructivos presentan más incidencias? (ej: andenes, luminarias, estructuras, accesos).



13\.	Ranking de elementos con mayor número de problemas.

BLOQUE 5 - ACCIONES Y GESTIÓN

14\.	¿Cuáles son las acciones pendientes más frecuentes en las actas?



15\.	¿Qué tipo de tareas suelen quedar sin resolver?





16\.	Agrupa las acciones por responsable (constructora, DF, subcontrata)

BLOQUE 6 - DESEMPEÑO DE OBRA

17\.	¿Qué obras presentan peor estado general según las actas?



18\.	Clasifica las obras en:

\- sin problemas

\- con incidencias leves

\- con incidencias graves

19\.	Resume el estado de los elementos constructivos mencionados (andenes, muros, …)



BLOQUE 7 – INSTALACIONES

20\.	¿Cuáles son los problemas más frecuentes en instalaciones eléctricas y luminarias?



21\.	¿Qué incumplimientos técnicos aparecen en verificaciones de equipos?



22\.	¿Qué equipos o soluciones presentan más incidencias técnicas?



23\.	Extrae las características técnicas de luminarias y equipos:

\- potencia

\- flujo luminoso

\- IP

\- tipo de instalación



24\.	Compara los equipos de instalaciones propuestos por la constructora indicando diferencias técnicas y eficiencia, en relación a los indicados en proyecto.

BLOQUE 8 - CUMPLIMIENTO NORMATIVO

25\.	¿Qué incumplimientos normativos se detectan en el conjunto de actas?



26\.	¿Qué requisitos técnicos no se cumplen con mayor frecuencia?



BLOQUE 9 – PLANIFICACIÓN Y RETRASOS

27\.	¿Cuáles son las principales causas de retraso en la obra?



28\.	¿Qué problemas afectan más a la planificación?



29\.	Extrae todas las fechas relevantes y eventos de planificación de obra (dataset de actas de obra correspondientes a una única obra).



30\.	Identifica hitos de obra y actividades programadas (dataset correspondiente a actas de obra de una única obra).



BLOQUE 10 - COMPARATIVA ENTRE OBRAS

31\.	Compara las diferentes obras en función del número de incidencias.



32\.	¿Qué obra tiene mayor número de problemas técnicos?



33\.	¿Qué diferencias hay entre estaciones en términos de estado e incidencias?





BLOQUE 11 — ACCIONES Y PENDIENTES

34\.	Extrae todas las acciones pendientes (para una única obra) indicando:

\- responsable.

\- acción.

\- contexto.

35\.	Lista todas las solicitudes realizadas a la constructora o técnicos.



Ejemplo:

•	“El contratista ha de aportar…”



BLOQUE 12 — VERIFICACIÓN TÉCNICA

36\.	Extrae el resultado de las verificaciones técnicas indicando:

\- elemento.

\- cumple / no cumple.

\- justificación

37\.	Identifica todos los requisitos técnicos evaluados y su conformidad



BLOQUE 13 — ANEXOS Y DOCUMENTACIÓN

38\.	Lista todos los documentos técnicos anexos mencionados en el acta.



QUERIES AVANZADAS

Analiza todo el dataset y genera:

1\.	Principales incidencias recurrentes.



2\.	Identifica patrones repetidos de incidencias en distintas obras.



3\.	Elementos más afectados / Determina los elementos con mayor número de incidencias (ej: andenes, luminarias).



4\.	Principales riesgos.



5\.	Acciones más frecuentes.



6\.	Estado general de las obras.



Detección de patrones

Identifica patrones repetidos en problemas técnicos entre distintas obras.

Insight automático

A partir de todas las actas, identifica oportunidades de mejora en la ejecución de obra.

Predicción

A partir de incidencias recurrentes, predice qué tipos de problemas pueden aparecer en futuras obras.











NOTA:

Dataset complejo: perfecto para NLP

Patrones claros: ideal para LLM

Queries adaptadas: listas para producción























ANEJO 

PROMPT GLOBAL (PARA TODO EL DATASET)



Eres un asistente experto en análisis técnico de actas de obra ferroviaria.

Analiza el conjunto completo de documentos proporcionados (actas, informes técnicos, verificaciones y reuniones) y genera un análisis global estructurado con los siguientes apartados:



1\. INCIDENCIAS

\- Identifica las incidencias más frecuentes en todas las actas.

\- Agrúpalas por tipología: estructural, instalaciones, seguridad, ejecución.

\- Indica ejemplos representativos.



2\. ELEMENTOS MÁS AFECTADOS

\- Identifica qué elementos presentan más problemas (andenes, luminarias, estructuras, accesos, etc.)

\- Genera un ranking.



3\. RIESGOS

\- Detecta riesgos relevantes para la seguridad, explotación o ejecución.

\- Indica riesgos críticos y su causa.



4\. ACCIONES Y PENDIENTES

\- Extrae las acciones pendientes más frecuentes.

\- Agrupa por responsable (constructora, dirección facultativa, otros).



5\. VERIFICACIONES TÉCNICAS

\- Resume los principales resultados de verificaciones (cumple / no cumple).

\- Detecta incumplimientos recurrentes.



6\. PLANIFICACIÓN Y RETRASOS

\- Identifica problemas recurrentes en planificación.

\- Detecta causas de retraso.





7\. TENDENCIAS

\- Detecta patrones que se repiten entre distintas actas u obras.

\- Identifica problemas sistémicos.



8\. ESTADO GLOBAL

\- Evalúa el estado general de las obras.

\- Clasifica: favorable / con incidencias / crítico.



9\. RECOMENDACIONES

\- Propón mejoras basadas en los problemas detectados.



Devuelve el resultado de forma clara, estructurada y priorizando insights relevantes.

















