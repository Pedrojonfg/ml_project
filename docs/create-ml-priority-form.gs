/**
 * Crea el Google Form de prioridades del project ML (BAM / IE).
 *
 * Cómo usarlo:
 * 1. Ve a https://script.google.com → New project
 * 2. Borra el código por defecto, pega TODO este archivo
 * 3. Guarda → selecciona createMlPriorityForm → Run
 * 4. Autoriza permisos la primera vez
 * 5. Ver → Logs (o Executions) para copiar la URL pública y la de edición
 *
 * Spec: docs/partner-priority-form-spec.md
 */
function createMlPriorityForm() {
  const form = FormApp.create('ML Project — Prioridades (intake)');

  form.setDescription(
    'Formulario para alinear prioridades del trabajo en grupo de Machine Learning ' +
      '(BAM · IE University).\n\n' +
      'Misma encuesta para ambos: texto libre primero, luego escalas. ' +
      'No pregunta por horas ni nivel técnico.\n\n' +
      'Escala 0–10: 0 = nada · 10 = muchísimo. ~8–10 min.'
  );
  form.setProgressBar(true);
  form.setConfirmationMessage(
    '¡Gracias! Con esto ya podemos buscar ideas de project y comentarlas.'
  );
  form.setAllowResponseEdits(true);
  form.setShuffleQuestions(false);
  // Opcional: descomenta si quieres 1 respuesta por cuenta Google
  // form.setLimitOneResponsePerUser(true);
  // form.setCollectEmail(true);

  const domains = [
    'Salud / biomedicina / omics',
    'Neurociencia / comportamiento / cognición',
    'Clima / energía / sostenibilidad',
    'Finanzas / economía / riesgo',
    'Física / ingeniería / sistemas dinámicos',
    'Robótica / control / percepción',
    'Computación cuántica / ML para ciencia “hard”',
    'Texto / lenguaje / redes sociales (NLP)',
    'Imagen / visión / señales',
    'Movilidad / ciudades / logística',
    'Deporte / rendimiento / wearables',
    'Educación / learning analytics',
    'Música / audio / creativo',
    'Metodológico / benchmarks (menos “dominio”, más método)',
  ];

  const methods = [
    'Modelos clásicos del temario (regresión, logistic, regularización, validación)',
    'Trees / random forests / boosting',
    'Kernels / SVM / kernel PCA',
    'Redes neuronales feedforward / autoencoders (PyTorch del curso)',
    'Probabilístico / Bayesian / Gaussian processes',
    'Unsupervised “rico” (mezclas, embeddings no lineales, etc.)',
    'Deep learning “heavy” (CNN, transformers, pipelines grandes)',
    'Physics-informed / modelos que respetan estructura física (PINNs, etc.)',
    'Reinforcement learning',
    'Generative (VAEs, difusión, LLMs como modelo, etc.)',
  ];

  // ——— Sección 1: Temáticas (texto libre) ———
  form
    .addTextItem()
    .setTitle('Nombre o alias')
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle(
      '¿Qué temas, dominios o tipos de problemas te interesan para el project de ML?'
    )
    .setHelpText(
      'Puede ser vago (“algo de salud”, “física”, “finanzas”) o concreto. ' +
        'No hace falta proponer el proyecto todavía.'
    )
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle(
      '¿Hay alguna idea a medias, dataset o paper que ya te dé curiosidad?'
    )
    .setHelpText('Si no, déjalo vacío.')
    .setRequired(false);

  // ——— Sección 2: Dominios 0–10 ———
  form
    .addPageBreakItem()
    .setTitle('Interés por dominio')
    .setHelpText(
      'Aunque hayas escrito arriba, puntúa de 0 a 10 cuánto te interesa cada dominio ' +
        'como contexto del project (no como problema concreto).'
    );

  domains.forEach(function (label) {
    form
      .addScaleItem()
      .setTitle(label)
      .setBounds(0, 10)
      .setLabels('Nada', 'Muchísimo')
      .setRequired(true);
  });

  form
    .addTextItem()
    .setTitle('Otro dominio no listado (nombre)')
    .setHelpText('Opcional. Si rellenas, puntúa la escala de abajo.')
    .setRequired(false);

  form
    .addScaleItem()
    .setTitle('Interés en ese “otro” dominio (0–10)')
    .setBounds(0, 10)
    .setLabels('Nada', 'Muchísimo')
    .setRequired(false);

  // ——— Sección 3: Intención / éxito ———
  form
    .addPageBreakItem()
    .setTitle('Intención y definición de éxito')
    .setHelpText(
      'Asumimos que queremos buena nota. Esto mide hacia dónde empujas el project.'
    );

  const priorities = [
    'Orientación laboral / portfolio (algo enseñable en entrevistas)',
    'Orientación investigación / profundidad teórica',
    'Impacto real / aplicado (que el problema “importe” fuera del aula)',
    'Aprendizaje técnico ambicioso (salir de la zona cómoda)',
    'Preferencia por un path fácil de articular con el temario (menos riesgo de nota)',
  ];

  priorities.forEach(function (label) {
    form
      .addScaleItem()
      .setTitle(label)
      .setBounds(0, 10)
      .setLabels('Nada', 'Muchísimo')
      .setRequired(true);
  });

  form
    .addParagraphTextItem()
    .setTitle('Para ti, ¿qué sería un 10 en este trabajo de grupo?')
    .setRequired(true);

  // ——— Sección 4: Fuera de temario + métodos ———
  form
    .addPageBreakItem()
    .setTitle('Fuera de temario y métodos (preferencia a priori)')
    .setHelpText(
      'No fija el paradigma del proyecto; solo preferencias. ' +
        'La elección fuerte de método se puede hacer después al mirar problemas concretos.'
    );

  form
    .addScaleItem()
    .setTitle(
      '¿Cuánto estás dispuesto/a a estudiar material fuera del temario para este project?'
    )
    .setBounds(0, 10)
    .setLabels('Nada', 'Muchísimo')
    .setRequired(true);

  form
    .addMultipleChoiceItem()
    .setTitle('Techo de compromiso fuera de temario')
    .setChoiceValues([
      'Solo leer blogs/docs/tutoriales cortos',
      'Implementar siguiendo tutoriales / repos existentes',
      'Leer papers e intentar reproducir ideas',
      'Intentar proponer / adaptar algo con sabor a investigación propia',
    ])
    .setRequired(true);

  form
    .addGridItem()
    .setTitle('Preferencia a priori por familia de métodos')
    .setHelpText('Una respuesta por fila.')
    .setRows(methods)
    .setColumns(['Me interesa', 'Me da igual', 'Preferiría evitar'])
    .setRequired(true);

  // ——— Sección 5: Vetos ———
  form
    .addPageBreakItem()
    .setTitle('Vetos')
    .setHelpText('Qué quieres evitar sí o sí.');

  form
    .addParagraphTextItem()
    .setTitle('¿Qué quieres evitar sí o sí en este project?')
    .setHelpText(
      'Dominios, tipos de problema, estilo (“otro Kaggle genérico”, “solo deep learning”, “nada de bio”…).'
    )
    .setRequired(true);

  form
    .addCheckboxItem()
    .setTitle(
      'Marca dominios que serían veto duro (aunque arriba hayas puesto interés medio)'
    )
    .setChoiceValues(domains.concat(['Ninguno']))
    .setRequired(false);

  form
    .addCheckboxItem()
    .setTitle('Marca métodos que serían veto duro')
    .setChoiceValues(methods.concat(['Ninguno']))
    .setRequired(false);

  // ——— Sección 6: Colaboración ———
  form
    .addPageBreakItem()
    .setTitle('Cómo preferirías trabajar')
    .setHelpText('Colaboración entre amigos; sin preguntas de horas ni skills.');

  form
    .addMultipleChoiceItem()
    .setTitle('Estilo de trabajo preferido')
    .setChoiceValues([
      'Bastante juntos (pair / sesiones compartidas)',
      'Dividir partes claras y juntar',
      'Mixto según la fase',
    ])
    .setRequired(true);

  form
    .addMultipleChoiceItem()
    .setTitle('Ritmo de coordinación')
    .setChoiceValues([
      'Check-ins frecuentes y cortos',
      'Bloques menos frecuentes pero más largos',
      'Flexible / según ruede',
    ])
    .setRequired(true);

  form
    .addMultipleChoiceItem()
    .setTitle('Si hay desacuerdo (tema, método, enfoque), ¿qué prefieres?')
    .setChoiceValues([
      'Discutir hasta consenso',
      'Probar rápido un spike y decidir con evidencia',
      'Que uno lidere esa decisión y el otro apoye',
    ])
    .showOtherOption(true)
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle('Cualquier otra cosa que deba saber antes de buscar ideas')
    .setRequired(false);

  const publishedUrl = form.getPublishedUrl();
  const editUrl = form.getEditUrl();

  Logger.log('=== FORM CREADO ===');
  Logger.log('URL para responder: ' + publishedUrl);
  Logger.log('URL para editar:    ' + editUrl);

  // También en un UI dialog si se ejecuta desde el editor
  try {
    SpreadsheetApp.getUi(); // puede fallar fuera de Sheets; ignorar
  } catch (e) {
    // no-op
  }

  return { publishedUrl: publishedUrl, editUrl: editUrl };
}
