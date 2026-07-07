const fallbackData = {
  user: {
    id: "USR-001",
    nombre: "Persona de prueba",
    runEnmascarado: "12.345.***-*",
    correo: "persona@example.cl",
    telefono: "+56 9 1234 5678",
    claveUnicaEstado: "activa demo",
    segundoFactorActivo: true,
    sesionesActivas: 3,
    demoAuth: {
      usuario: "demo.claveunica",
      clave: "DemoLocal2026",
      otp: "123456"
    },
    personalSecurity: {
      metodo: "codigo demo",
      codigoDemo: "123456"
    },
    ddu: {
      estado: "pendiente",
      domicilio: "Domicilio Digital Único pendiente de confirmación",
      alertaPendiente: true,
      fechaConfiguracion: "",
      canal: "",
      casillaDemo: ""
    }
  },
  ddu: {
    estado: "pendiente",
    domicilio: "Domicilio Digital Unico pendiente de configuracion demo",
    alertaPendiente: true,
    fechaConfiguracion: "",
    canal: "",
    casillaDemo: "",
    pasarela: {
      nombre: "Pasarela simulada de configuracion DDU",
      advertencia: "No es CasillaUnica real y no configura DDU real."
    }
  },
  sessions: [
    {
      id: "SES-DEMO-001",
      actual: true,
      dispositivo: "Notebook institucional demo",
      navegador: "Navegador local",
      ubicacion: "Ubicacion generica demo",
      ultimoAcceso: "2026-07-05 10:15",
      estado: "activa",
      riesgo: ""
    },
    {
      id: "SES-DEMO-002",
      actual: false,
      dispositivo: "Telefono demo",
      navegador: "Navegador movil simulado",
      ubicacion: "Zona generica norte",
      ultimoAcceso: "2026-07-04 18:40",
      estado: "activa",
      riesgo: "revision recomendada"
    },
    {
      id: "SES-DEMO-003",
      actual: false,
      dispositivo: "Equipo compartido demo",
      navegador: "Navegador de escritorio simulado",
      ubicacion: "Zona generica centro",
      ultimoAcceso: "2026-07-03 09:25",
      estado: "activa",
      riesgo: "riesgo medio demo"
    }
  ],
  notifications: [
    {
      id: "NOT-001",
      institucion: "Servicio Demo de Beneficios",
      titulo: "Aviso de beneficio local disponible",
      estado: "pendiente",
      fechaRecepcion: "2026-07-05 09:30",
      prioridad: "media",
      categoria: "informativa",
      contenido: "Contenido ficticio seguro para validar el detalle local de una notificacion demo."
    },
    {
      id: "NOT-002",
      institucion: "Unidad Demo de Tramites",
      titulo: "Recordatorio de tramite simulado",
      estado: "pendiente",
      fechaRecepcion: "2026-07-04 16:20",
      prioridad: "alta",
      categoria: "recordatorio",
      contenido: "Mensaje local de prueba sin documentos reales, datos personales reales ni enlaces productivos."
    }
  ],
  authorizations: [
    {
      id: "AUT-DEMO-001",
      institucion: "Instituto Demo de Estudios Sociales",
      finalidad: "Validar postulacion ficticia a un beneficio local de prueba.",
      tipoDato: "Indicador sensible generico",
      fechaSolicitud: "2026-07-02 09:15",
      estado: "pendiente",
      fechaDecision: "",
      historial: ["2026-07-02 09:15 solicitud demo recibida"]
    },
    {
      id: "AUT-DEMO-002",
      institucion: "Agencia Ficticia de Orientacion Ciudadana",
      finalidad: "Preparar recomendacion simulada para un tramite ciudadano demo.",
      tipoDato: "Categoria sensible generica",
      fechaSolicitud: "2026-07-03 11:40",
      estado: "pendiente",
      fechaDecision: "",
      historial: ["2026-07-03 11:40 solicitud demo recibida"]
    },
    {
      id: "AUT-DEMO-003",
      institucion: "Centro Demo de Apoyo Local",
      finalidad: "Revisar elegibilidad ficticia de acompanamiento no productivo.",
      tipoDato: "Antecedente sensible representado de forma generica",
      fechaSolicitud: "2026-06-28 15:05",
      estado: "aprobada",
      fechaDecision: "2026-06-29 10:00",
      historial: [
        "2026-06-28 15:05 solicitud demo recibida",
        "2026-06-29 10:00 aprobacion demo registrada"
      ]
    },
    {
      id: "AUT-DEMO-004",
      institucion: "Unidad Simulada de Servicios Comunitarios",
      finalidad: "Contrastar requisito ficticio para una atencion local de prueba.",
      tipoDato: "Dato sensible generico no revelado",
      fechaSolicitud: "2026-06-25 13:30",
      estado: "rechazada",
      fechaDecision: "2026-06-25 18:20",
      historial: [
        "2026-06-25 13:30 solicitud demo recibida",
        "2026-06-25 18:20 rechazo demo registrado"
      ]
    },
    {
      id: "AUT-DEMO-005",
      institucion: "Programa Ficticio de Asistencia Digital",
      finalidad: "Mantener referencia simulada para una revision historica local.",
      tipoDato: "Grupo sensible generico",
      fechaSolicitud: "2026-06-20 08:50",
      estado: "revocada",
      fechaDecision: "2026-06-30 16:10",
      historial: [
        "2026-06-20 08:50 solicitud demo recibida",
        "2026-06-21 09:25 aprobacion demo registrada",
        "2026-06-30 16:10 revocacion demo registrada"
      ]
    }
  ]
};

const state = {
  data: fallbackData,
  isPrivate: sessionStorage.getItem("claveunica_demo_auth") === "1",
  pendingUserId: sessionStorage.getItem("claveunica_demo_pending_user") || "",
  loginError: "",
  otpError: "",
  personalDataMessage: null,
  sessionMessage: null,
  dduMessage: null,
  dduModalOpen: false,
  dduGatewayCancelConfirm: false,
  notificationMessage: null,
  selectedNotificationId: "",
  authorizationMessage: null,
  selectedAuthorizationId: ""
};

const NOTIFICATION_READ_STORAGE_KEY = "claveunica_demo_notification_reads";
const AUTHORIZATION_STORAGE_KEY = "claveunica_demo_authorization_state";

const privateRoutes = [
  ["dashboard", "Dashboard"],
  ["datos-personales", "Datos personales"],
  ["2fa", "2FA"],
  ["sesiones", "Sesiones"],
  ["ddu", "DDU"],
  ["notificaciones", "Notificaciones"],
  ["autorizaciones", "Autorizaciones"]
];

const app = document.querySelector("#app");

async function loadMocks() {
  try {
    const [user, notifications, authorizations, sessions, ddu] = await Promise.all([
      fetch("../mocks/user.json").then((response) => response.json()),
      fetch("../mocks/notifications.json").then((response) => response.json()),
      fetch("../mocks/authorizations.json").then((response) => response.json()),
      fetch("../mocks/sessions.json").then((response) => response.json()),
      fetch("../mocks/ddu.json").then((response) => response.json())
    ]);
    state.data = { user: { ...user, ddu }, notifications, authorizations, sessions, ddu };
  } catch {
    state.data = fallbackData;
  }
  applyStoredDduState();
  applyStoredNotificationState();
  applyStoredAuthorizationState();
}

function applyStoredDduState() {
  const stored = sessionStorage.getItem("claveunica_demo_ddu_state");
  if (!stored) return;

  try {
    const parsed = JSON.parse(stored);
    if (parsed && (parsed.estado === "pendiente" || parsed.estado === "configurado")) {
      state.data.ddu = { ...(state.data.ddu || fallbackData.ddu), ...parsed };
      state.data.user.ddu = state.data.ddu;
    }
  } catch {
    sessionStorage.removeItem("claveunica_demo_ddu_state");
  }
}

function getDduState() {
  return state.data.ddu || state.data.user.ddu || fallbackData.ddu;
}

function applyStoredNotificationState() {
  const stored = sessionStorage.getItem(NOTIFICATION_READ_STORAGE_KEY);
  if (!stored) return;

  try {
    const readIds = JSON.parse(stored);
    if (!Array.isArray(readIds)) return;

    state.data.notifications = (state.data.notifications || []).map((item) => (
      readIds.includes(item.id) ? { ...item, estado: "leida demo" } : item
    ));
  } catch {
    sessionStorage.removeItem(NOTIFICATION_READ_STORAGE_KEY);
  }
}

function isNotificationRead(item) {
  return item.estado === "leida demo" || item.estado === "leida";
}

function getPendingNotifications() {
  return (state.data.notifications || []).filter((item) => !isNotificationRead(item));
}

function saveReadNotifications() {
  const readIds = (state.data.notifications || [])
    .filter((item) => isNotificationRead(item))
    .map((item) => item.id);
  sessionStorage.setItem(NOTIFICATION_READ_STORAGE_KEY, JSON.stringify(readIds));
}

function applyStoredAuthorizationState() {
  const stored = sessionStorage.getItem(AUTHORIZATION_STORAGE_KEY);
  if (!stored) return;

  try {
    const storedItems = JSON.parse(stored);
    if (!Array.isArray(storedItems)) return;

    state.data.authorizations = (state.data.authorizations || []).map((item) => {
      const storedItem = storedItems.find((entry) => entry.id === item.id);
      return storedItem ? { ...item, ...storedItem } : item;
    });
  } catch {
    sessionStorage.removeItem(AUTHORIZATION_STORAGE_KEY);
  }
}

function saveAuthorizationState() {
  const storedItems = (state.data.authorizations || []).map((item) => ({
    id: item.id,
    estado: item.estado,
    fechaDecision: item.fechaDecision || "",
    historial: item.historial || []
  }));
  sessionStorage.setItem(AUTHORIZATION_STORAGE_KEY, JSON.stringify(storedItems));
}

function getAuthorizationCounts() {
  const items = state.data.authorizations || [];
  return {
    pendientes: items.filter((item) => item.estado === "pendiente").length,
    vigentes: items.filter((item) => item.estado === "aprobada").length,
    rechazadas: items.filter((item) => item.estado === "rechazada").length,
    revocadas: items.filter((item) => item.estado === "revocada").length
  };
}

function updateDduState(nextDdu) {
  state.data.ddu = { ...getDduState(), ...nextDdu };
  state.data.user.ddu = state.data.ddu;
  sessionStorage.setItem("claveunica_demo_ddu_state", JSON.stringify(state.data.ddu));
}

function setPrivateMode(enabled) {
  state.isPrivate = enabled;
  state.pendingUserId = "";
  state.loginError = "";
  state.otpError = "";

  if (enabled) {
    sessionStorage.setItem("claveunica_demo_auth", "1");
    sessionStorage.removeItem("claveunica_demo_pending_user");
    window.location.hash = "#/dashboard";
    return;
  }

  sessionStorage.removeItem("claveunica_demo_auth");
  sessionStorage.removeItem("claveunica_demo_pending_user");
  window.location.hash = "#/inicio";
}

function beginLogin() {
  state.loginError = "";
  state.otpError = "";
  window.location.hash = state.isPrivate ? "#/dashboard" : "#/login";
}

function publicHome() {
  const unread = getPendingNotifications().length;
  return `
    <section class="hero" aria-labelledby="portal-title">
      <div>
        <h1 id="portal-title">Portal Ciudadano de ClaveÚnica</h1>
        <p>Acceso local de prototipo para activar, autenticar, recuperar y revisar información pública del servicio.</p>
        <div class="action-grid" aria-label="Accesos principales">
          <button class="action" type="button" data-action="activate">Activar ClaveÚnica</button>
          <button class="action" type="button" data-action="login">Iniciar sesión</button>
          <button class="action secondary" type="button" data-action="recover">Recuperar ClaveÚnica</button>
          <a class="action secondary" href="#/ayuda">Ayuda</a>
          <a class="action secondary" href="#/novedades">Novedades</a>
        </div>
      </div>
      <aside class="status-panel" aria-label="Resumen del prototipo">
        <h2>Estado local</h2>
        <dl class="metric-list">
          <div><dt>Usuario mock</dt><dd>${state.data.user.nombre}</dd></div>
          <div><dt>DDU</dt><dd>${state.data.user.ddu.estado}</dd></div>
          <div><dt>CasillaUnica demo</dt><dd>${unread} pendiente</dd></div>
        </dl>
      </aside>
    </section>
  `;
}

function publicInfo(kind) {
  const title = kind === "ayuda" ? "Ayuda" : "Novedades";
  const body = kind === "ayuda"
    ? "Canales de soporte y orientación del portal público."
    : "Actualizaciones informativas visibles antes de iniciar sesión.";
  return `
    <section class="hero" aria-labelledby="public-title">
      <div>
        <h1 id="public-title">${title}</h1>
        <p>${body}</p>
        <div class="action-grid">
          <a class="action" href="#/inicio">Volver al portal</a>
          <button class="action secondary" type="button" data-action="login">Iniciar sesión</button>
        </div>
      </div>
    </section>
  `;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function loginView() {
  return `
    <section class="auth-layout" aria-labelledby="login-title">
      <div class="auth-copy">
        <span class="tag">Prototipo local</span>
        <h1 id="login-title">Iniciar sesión</h1>
        <p>Flujo simulado para validar la experiencia de acceso del Portal Ciudadano de ClaveÚnica. No conecta con ClaveÚnica real.</p>
      </div>
      <form class="auth-card" id="login-form" autocomplete="off" novalidate>
        <div class="form-field">
          <label for="login-user">Usuario demo</label>
          <input id="login-user" name="usuario" type="text" inputmode="email" required>
        </div>
        <div class="form-field">
          <label for="login-password">Clave demo</label>
          <input id="login-password" name="clave" type="password" required>
        </div>
        ${state.loginError ? `<p class="form-error" role="alert">${state.loginError}</p>` : ""}
        <button class="primary-button" type="submit">Continuar</button>
        <button class="link-button auth-link" type="button" data-action="recover">Recuperar ClaveÚnica</button>
      </form>
    </section>
  `;
}

function otpView() {
  return `
    <section class="auth-layout" aria-labelledby="otp-title">
      <div class="auth-copy">
        <span class="tag">Segundo factor</span>
        <h1 id="otp-title">Verificación 2FA</h1>
        <p>Ingresa el código OTP simulado definido en el mock local para completar el inicio de sesión.</p>
      </div>
      <form class="auth-card" id="otp-form" autocomplete="off" novalidate>
        <div class="form-field">
          <label for="otp-code">Código OTP demo</label>
          <input id="otp-code" name="otp" type="text" inputmode="numeric" maxlength="6" required>
        </div>
        ${state.otpError ? `<p class="form-error" role="alert">${state.otpError}</p>` : ""}
        <button class="primary-button" type="submit">Validar código</button>
        <button class="link-button auth-link" type="button" data-action="login">Volver al login</button>
      </form>
    </section>
  `;
}

function privateShell(route) {
  const nav = privateRoutes.map(([key, label]) => {
    const active = route === key ? " class=\"active\"" : "";
    return `<a${active} href="#/${key}">${label}</a>`;
  }).join("");

  return `
    <section class="private-layout">
      <aside class="private-aside">
        <nav class="private-nav" aria-label="Navegación privada">${nav}</nav>
        <button class="link-button" type="button" data-action="logout">Cerrar sesión</button>
      </aside>
      <div class="private-main">${privateContent(route)}</div>
    </section>
  `;
}

function privateContent(route) {
  if (route === "dashboard") {
    const pendingAuth = state.data.authorizations.filter((item) => item.estado === "pendiente").length;
    const ddu = getDduState();
    const dduSummary = ddu.estado === "configurado"
      ? `Configurado localmente el ${escapeHtml(ddu.fechaConfiguracion)} mediante ${escapeHtml(ddu.canal)}.`
      : "Configuracion DDU pendiente en estado demo/local.";
    const pendingNotifications = getPendingNotifications().length;
    const notificationSummary = ddu.estado === "configurado"
      ? `${pendingNotifications} notificacion(es) pendiente(s) en CasillaUnica simulada/local.`
      : "Notificaciones bloqueadas hasta configurar DDU demo/local.";
    return `
      <section class="panel" aria-labelledby="dashboard-title">
        <h2 id="dashboard-title">Dashboard privado</h2>
        <div class="summary-grid">
          <div><span>Persona</span><strong>${state.data.user.nombre}</strong></div>
          <div><span>DDU</span><strong>${escapeHtml(ddu.estado)}</strong></div>
          <div><span>2FA</span><strong>${state.data.user.segundoFactorActivo ? "activo" : "inactivo"}</strong></div>
        </div>
        <div class="section-box">
          <span class="tag">Resumen</span>
          <p>${escapeHtml(ddu.domicilio)}</p>
          <p>${dduSummary}</p>
          <p>${notificationSummary} ${pendingAuth} autorizacion(es) pendiente(s).</p>
        </div>
        <div class="dashboard-actions" aria-label="Accesos privados">
          <a class="action compact" href="#/datos-personales">Datos personales</a>
          <a class="action compact" href="#/sesiones">Sesiones</a>
          <a class="action compact" href="#/ddu">DDU</a>
          <a class="action compact" href="#/notificaciones">Notificaciones</a>
          <a class="action compact" href="#/autorizaciones">Autorizaciones</a>
        </div>
      </section>
    `;
  }

  if (route === "datos-personales") {
    return personalDataView();
  }

  if (route === "sesiones") {
    return sessionsView();
  }

  if (route === "ddu") {
    return dduView();
  }

  if (route === "ddu-configuracion-demo") {
    return dduGatewayView();
  }

  if (route === "notificaciones") {
    return notificationsView();
  }

  if (route === "autorizaciones") {
    return authorizationsView();
  }

  if (route === "autorizaciones") {
    return `
      <section class="panel" aria-labelledby="authorizations-title">
        <h2 id="authorizations-title">Autorizaciones</h2>
        <ul class="notice-list">
          ${state.data.authorizations.map((item) => `<li><strong>${item.institucion}</strong><br>${item.tipo} · ${item.estado}</li>`).join("")}
        </ul>
      </section>
    `;
  }

  const label = privateRoutes.find(([key]) => key === route)?.[1] || "Dashboard";
  return `
    <section class="panel" aria-labelledby="section-title">
      <h2 id="section-title">${label}</h2>
      <div class="section-box">
        <span class="tag">pendiente</span>
        <p>Navegación preparada para el módulo.</p>
      </div>
    </section>
  `;
}

function authorizationsView() {
  const selected = (state.data.authorizations || []).find((item) => item.id === state.selectedAuthorizationId);
  const message = state.authorizationMessage
    ? `<p class="form-${state.authorizationMessage.type}" role="alert">${state.authorizationMessage.text}</p>`
    : "";

  if (selected) {
    return authorizationDetailView(selected, message);
  }

  return authorizationListView(message);
}

function authorizationListView(message) {
  const counts = getAuthorizationCounts();
  const items = state.data.authorizations || [];
  const list = items.length
    ? items.map((item) => authorizationCard(item)).join("")
    : `
      <div class="section-box">
        <span class="tag">sin solicitudes</span>
        <p>No hay autorizaciones demo en el estado local del prototipo.</p>
      </div>
    `;

  return `
    <section class="panel authorizations-panel" aria-labelledby="authorizations-title">
      <div class="panel-heading">
        <div>
          <span class="tag">simulado/local</span>
          <h2 id="authorizations-title">Autorizaciones</h2>
        </div>
        <a class="link-button" href="#/dashboard">Volver al dashboard</a>
      </div>

      <div class="section-box warning-box" role="note">
        <strong>Modulo Autorizaciones de datos sensibles simulado/local</strong>
        <p>No usa autorizaciones reales, no muestra datos sensibles reales, no valida efectos legales, no conecta servicios del Estado y no persiste cambios en backend.</p>
      </div>

      <div class="summary-grid authorizations-summary" aria-label="Resumen de autorizaciones por estado">
        <div><span>pendientes</span><strong>${counts.pendientes}</strong></div>
        <div><span>aprobadas/vigentes</span><strong>${counts.vigentes}</strong></div>
        <div><span>rechazadas</span><strong>${counts.rechazadas}</strong></div>
        <div><span>revocadas</span><strong>${counts.revocadas}</strong></div>
      </div>

      ${message}
      <div class="section-box">
        <div class="list-heading">
          <h3>Lista mock de autorizaciones</h3>
          <span class="tag">sessionStorage demo/local</span>
        </div>
        <div class="authorizations-list" aria-label="Lista mock de autorizaciones">
          ${list}
        </div>
      </div>
    </section>
  `;
}

function authorizationCard(item) {
  return `
    <article class="authorization-card" aria-label="Autorizacion ${escapeHtml(item.estado)}">
      <div>
        <h3>${escapeHtml(item.id)}</h3>
        <dl class="authorization-details">
          <div><dt>Institucion solicitante ficticia</dt><dd>${escapeHtml(item.institucion || "Institucion demo")}</dd></div>
          <div><dt>Finalidad declarada</dt><dd>${escapeHtml(item.finalidad || "Finalidad demo")}</dd></div>
          <div><dt>Tipo de dato sensible generico</dt><dd>${escapeHtml(item.tipoDato || item.tipo || "Dato sensible generico")}</dd></div>
          <div><dt>Fecha de solicitud ficticia</dt><dd>${escapeHtml(item.fechaSolicitud || "sin fecha")}</dd></div>
          <div><dt>Estado</dt><dd>${escapeHtml(item.estado)}</dd></div>
          <div><dt>Fecha de decision</dt><dd>${escapeHtml(item.fechaDecision || "sin decision")}</dd></div>
        </dl>
      </div>
      <button class="primary-button authorization-open-button" type="button" data-action="open-authorization" data-authorization-id="${escapeHtml(item.id)}">Abrir detalle</button>
    </article>
  `;
}

function authorizationDetailView(item, message) {
  const isPending = item.estado === "pendiente";
  const isActive = item.estado === "aprobada";
  const readOnly = !isPending && !isActive;
  const history = (item.historial || []).map((entry) => `<li>${escapeHtml(entry)}</li>`).join("");
  const actionForm = (isPending || isActive)
    ? `
      <form class="section-box authorization-form" id="authorization-decision-form" data-authorization-id="${escapeHtml(item.id)}" autocomplete="off" novalidate>
        <div class="form-intro">
          <span class="tag">factor demo obligatorio</span>
          <p>Para aprobar, rechazar o revocar se exige el factor demo. Esta accion solo modifica el estado local del navegador.</p>
        </div>
        <div class="form-field security-factor-field">
          <label for="authorization-security-code">Factor demo obligatorio</label>
          <input id="authorization-security-code" name="factor" type="text" inputmode="numeric" maxlength="6" placeholder="Codigo demo" required>
        </div>
        <div class="form-actions">
          ${isPending ? `<button class="primary-button authorization-action-button" type="submit" data-authorization-decision="aprobar">Aprobar solicitud</button>` : ""}
          ${isPending ? `<button class="link-button" type="submit" data-authorization-decision="rechazar">Rechazar solicitud</button>` : ""}
          ${isActive ? `<button class="primary-button authorization-action-button" type="submit" data-authorization-decision="revocar">Revocar autorizacion</button>` : ""}
        </div>
      </form>
    `
    : `
      <div class="section-box">
        <span class="tag">solo lectura</span>
        <p>Las autorizaciones rechazadas o revocadas quedan solo lectura en este prototipo local.</p>
      </div>
    `;

  return `
    <section class="panel authorizations-panel" aria-labelledby="authorization-detail-title">
      <div class="panel-heading">
        <div>
          <span class="tag">detalle simulado/local</span>
          <h2 id="authorization-detail-title">Detalle de autorizacion ${escapeHtml(item.id)}</h2>
        </div>
        <a class="link-button" href="#/dashboard">Volver al dashboard</a>
      </div>

      <div class="section-box warning-box" role="note">
        <strong>Detalle sin datos sensibles reales</strong>
        <p>La institucion, finalidad, tipo de dato y decision son ficticios. No hay autorizacion legalmente valida ni conexion real con sistemas del Estado.</p>
      </div>

      ${message}
      <dl class="summary-grid authorization-detail-grid" aria-label="Detalle de autorizacion demo">
        <div><span>ID ficticio</span><strong>${escapeHtml(item.id)}</strong></div>
        <div><span>Institucion solicitante ficticia</span><strong>${escapeHtml(item.institucion || "Institucion demo")}</strong></div>
        <div><span>Estado</span><strong>${escapeHtml(item.estado)}</strong></div>
        <div><span>Fecha de solicitud ficticia</span><strong>${escapeHtml(item.fechaSolicitud || "sin fecha")}</strong></div>
        <div><span>Fecha de decision</span><strong>${escapeHtml(item.fechaDecision || "sin decision")}</strong></div>
        <div><span>Dato sensible representado</span><strong>${escapeHtml(item.tipoDato || item.tipo || "Dato sensible generico")}</strong></div>
      </dl>

      <article class="section-box">
        <span class="tag">finalidad declarada</span>
        <p>${escapeHtml(item.finalidad || "Finalidad demo para validacion local.")}</p>
      </article>

      ${actionForm}

      <div class="section-box authorization-history">
        <div class="list-heading">
          <h3>Historial local de autorizacion</h3>
          <span class="tag">${readOnly ? "solo lectura" : "editable local"}</span>
        </div>
        <ul>${history}</ul>
      </div>

      <div class="form-actions">
        <button class="link-button" type="button" data-action="back-authorization-list">Volver al listado</button>
      </div>
    </section>
  `;
}

function notificationsView() {
  const ddu = getDduState();
  const isConfigured = ddu.estado === "configurado";
  const selected = (state.data.notifications || []).find((item) => item.id === state.selectedNotificationId);
  const message = state.notificationMessage
    ? `<p class="form-${state.notificationMessage.type}" role="alert">${state.notificationMessage.text}</p>`
    : "";

  if (!isConfigured) {
    return `
      <section class="panel notifications-panel" aria-labelledby="notifications-title">
        <div class="panel-heading">
          <div>
            <span class="tag">simulacion local</span>
            <h2 id="notifications-title">Notificaciones</h2>
          </div>
          <a class="link-button" href="#/dashboard">Volver al dashboard</a>
        </div>
        <div class="section-box warning-box notifications-ddu-alert" role="alert">
          <strong>DDU pendiente requerido</strong>
          <p>Debes configurar el Domicilio Digital Unico demo antes de visualizar notificaciones. No se muestra listado mientras el DDU esta pendiente/no configurado.</p>
          <div class="form-actions">
            <a class="action compact" href="#/ddu">Ir a DDU</a>
          </div>
        </div>
      </section>
    `;
  }

  if (selected) {
    return notificationDetailView(selected, message);
  }

  return notificationListView(message);
}

function notificationListView(message) {
  const pending = getPendingNotifications();
  const list = pending.length
    ? pending.map((item) => notificationCard(item)).join("")
    : `
      <div class="section-box">
        <span class="tag">sin pendientes</span>
        <p>No hay notificaciones pendientes de lectura en el estado demo/local.</p>
      </div>
    `;

  return `
    <section class="panel notifications-panel" aria-labelledby="notifications-title">
      <div class="panel-heading">
        <div>
          <span class="tag">CasillaUnica simulada/local</span>
          <h2 id="notifications-title">Notificaciones</h2>
        </div>
        <a class="link-button" href="#/dashboard">Volver al dashboard</a>
      </div>

      <div class="section-box warning-box" role="note">
        <strong>Modulo Notificaciones simulado/local</strong>
        <p>No usa Plataforma de Notificaciones real, no usa CasillaUnica real, no carga notificaciones reales y no persiste cambios en backend.</p>
      </div>

      <div class="summary-grid notifications-summary" aria-label="Resumen de notificaciones demo">
        <div><span>DDU</span><strong>configurado</strong></div>
        <div><span>Pendientes de lectura</span><strong>${pending.length}</strong></div>
        <div><span>Persistencia</span><strong>sessionStorage demo/local</strong></div>
      </div>

      ${message}
      <div class="notifications-list" aria-label="Listado de notificaciones pendientes">
        ${list}
      </div>
    </section>
  `;
}

function notificationCard(item) {
  return `
    <article class="notification-card" aria-label="Notificacion pendiente">
      <div>
        <h3>${escapeHtml(item.titulo || item.asunto || "Notificacion demo")}</h3>
        <dl class="notification-details">
          <div><dt>Fecha de recepcion ficticia</dt><dd>${escapeHtml(item.fechaRecepcion || item.fecha || "sin fecha")}</dd></div>
          <div><dt>Institucion remitente ficticia</dt><dd>${escapeHtml(item.institucion || item.origen || "Institucion demo")}</dd></div>
          <div><dt>Estado</dt><dd>${escapeHtml(item.estado)}</dd></div>
          <div><dt>Prioridad/categoria</dt><dd>${escapeHtml(item.prioridad || item.categoria || "informativa")}</dd></div>
        </dl>
      </div>
      <button class="primary-button notification-open-button" type="button" data-action="open-notification" data-notification-id="${escapeHtml(item.id)}">Abrir detalle</button>
    </article>
  `;
}

function notificationDetailView(item, message) {
  const isRead = isNotificationRead(item);

  return `
    <section class="panel notifications-panel" aria-labelledby="notification-detail-title">
      <div class="panel-heading">
        <div>
          <span class="tag">derivacion simulada/local a CasillaUnica</span>
          <h2 id="notification-detail-title">${escapeHtml(item.titulo || "Detalle de notificacion")}</h2>
        </div>
        <a class="link-button" href="#/dashboard">Volver al dashboard</a>
      </div>

      <div class="section-box warning-box" role="note">
        <strong>Detalle local seguro</strong>
        <p>Esta pantalla representa una derivacion simulada a CasillaUnica. No abre URLs productivas, no consulta servicios externos y no contiene documentos reales.</p>
      </div>

      ${message}
      <dl class="summary-grid notifications-summary" aria-label="Detalle de notificacion demo">
        <div><span>Fecha de recepcion ficticia</span><strong>${escapeHtml(item.fechaRecepcion || item.fecha || "sin fecha")}</strong></div>
        <div><span>Institucion remitente ficticia</span><strong>${escapeHtml(item.institucion || item.origen || "Institucion demo")}</strong></div>
        <div><span>Estado</span><strong>${escapeHtml(item.estado)}</strong></div>
      </dl>

      <article class="section-box notification-body">
        <span class="tag">${escapeHtml(item.prioridad || item.categoria || "informativa")}</span>
        <p>${escapeHtml(item.contenido || "Contenido ficticio seguro para validacion local.")}</p>
      </article>

      <div class="form-actions">
        <button class="primary-button notification-read-button" type="button" data-action="mark-notification-read" data-notification-id="${escapeHtml(item.id)}" ${isRead ? "disabled" : ""}>${isRead ? "Notificacion leida" : "Marcar como leida"}</button>
        <button class="link-button" type="button" data-action="back-notification-list">Volver al listado</button>
      </div>
    </section>
  `;
}

function dduView() {
  const ddu = getDduState();
  const isConfigured = ddu.estado === "configurado";
  const message = state.dduMessage
    ? `<p class="form-${state.dduMessage.type}" role="alert">${state.dduMessage.text}</p>`
    : "";
  const pendingAlert = !isConfigured
    ? `
      <div class="section-box warning-box ddu-pending-alert" role="alert">
        <strong>Alerta de configuracion pendiente</strong>
        <p>El Domicilio Digital Unico esta pendiente/no configurado en este prototipo local. No uses domicilio real ni datos personales reales.</p>
      </div>
    `
    : "";
  const configuredAccess = isConfigured
    ? `
      <div class="section-box">
        <span class="tag">acceso preparado</span>
        <p>El acceso hacia Notificaciones queda preparado como placeholder local. No hay conexion real con Plataforma de Notificaciones ni CasillaUnica.</p>
        <a class="action compact" href="#/notificaciones">Ir a Notificaciones</a>
      </div>
    `
    : "";
  const primaryAction = isConfigured
    ? `<a class="action compact" href="#/notificaciones">Revisar notificaciones preparadas</a>`
    : `<button class="primary-button ddu-start-button" type="button" data-action="open-ddu-confirmation">Iniciar configuracion DDU</button>`;

  return `
    <section class="panel ddu-panel" aria-labelledby="ddu-title">
      <div class="panel-heading">
        <div>
          <span class="tag">simulacion local</span>
          <h2 id="ddu-title">Domicilio Digital Unico (DDU)</h2>
        </div>
        <a class="link-button" href="#/dashboard">Volver al dashboard</a>
      </div>

      <div class="section-box warning-box" role="note">
        <strong>Modulo DDU simulado/local</strong>
        <p>Esta pantalla no usa CasillaUnica real, no configura DDU real, no llama servicios externos y no persiste datos en backend.</p>
      </div>

      ${message}
      ${pendingAlert}

      <div class="summary-grid ddu-status-grid" aria-label="Estado actual del DDU">
        <div><span>Estado DDU</span><strong>${escapeHtml(ddu.estado)}</strong></div>
        <div><span>Fecha ficticia</span><strong>${escapeHtml(ddu.fechaConfiguracion || "sin configurar")}</strong></div>
        <div><span>Canal/casilla demo</span><strong>${escapeHtml(ddu.casillaDemo || "pendiente")}</strong></div>
      </div>

      <div class="section-box">
        <p>${escapeHtml(ddu.domicilio)}</p>
        <div class="form-actions">${primaryAction}</div>
      </div>

      ${configuredAccess}
      ${state.dduModalOpen ? dduConfirmationModal() : ""}
    </section>
  `;
}

function dduConfirmationModal() {
  return `
    <div class="modal-backdrop" role="presentation">
      <section class="modal-dialog" role="dialog" aria-modal="true" aria-labelledby="ddu-modal-title">
        <span class="tag">confirmacion requerida</span>
        <h3 id="ddu-modal-title">Confirmar derivacion simulada DDU</h3>
        <p>Continuaras a una pasarela simulada de configuracion DDU. No es CasillaUnica real y no se configurara ningun domicilio digital real.</p>
        <div class="form-actions">
          <button class="primary-button" type="button" data-action="continue-ddu-gateway">Continuar a pasarela simulada</button>
          <button class="link-button" type="button" data-action="cancel-ddu-modal">Cancelar y volver al DDU</button>
        </div>
      </section>
    </div>
  `;
}

function dduGatewayView() {
  const ddu = getDduState();
  const cancelConfirm = state.dduGatewayCancelConfirm
    ? `
      <div class="section-box warning-box" role="alert">
        <strong>Confirmar cancelacion</strong>
        <p>Si cancelas, retornaras a la seccion DDU y el estado seguira pendiente/no configurado.</p>
        <div class="form-actions">
          <button class="primary-button" type="button" data-action="confirm-ddu-gateway-cancel">Si, cancelar configuracion</button>
          <button class="link-button" type="button" data-action="keep-ddu-gateway">Seguir en pasarela simulada</button>
        </div>
      </div>
    `
    : "";

  return `
    <section class="auth-layout ddu-gateway" aria-labelledby="ddu-gateway-title">
      <div class="auth-copy">
        <span class="tag">pasarela simulada</span>
        <h1 id="ddu-gateway-title">Pasarela simulada de configuracion DDU</h1>
        <p>No es CasillaUnica real, no configura DDU real y no envia datos a servicios externos. Todo queda en estado demo/local del navegador.</p>
      </div>
      <form class="auth-card" id="ddu-gateway-form" autocomplete="off" novalidate>
        <div class="form-intro">
          <span class="tag">sin domicilio real</span>
          <p>Confirma una activacion demo con casilla ficticia. No ingreses domicilio real, correo real ni telefono real.</p>
        </div>
        <div class="form-field">
          <label for="ddu-demo-channel">Canal/casilla demo</label>
          <input id="ddu-demo-channel" name="canalDemo" type="text" value="${escapeHtml(ddu.casillaDemo || "DDU-LOCAL-001")}" readonly>
        </div>
        ${cancelConfirm}
        <div class="form-actions">
          <button class="primary-button" type="submit">Completar configuracion demo</button>
          <button class="link-button" type="button" data-action="request-ddu-gateway-cancel">Cancelar configuracion</button>
          <a class="link-button" href="#/dashboard">Retornar al portal</a>
        </div>
      </form>
    </section>
  `;
}

function sessionsView() {
  const sessions = state.data.sessions || [];
  const activeSessions = sessions.filter((item) => item.estado !== "cerrada demo");
  const currentSession = activeSessions.find((item) => item.actual);
  const message = state.sessionMessage
    ? `<p class="form-${state.sessionMessage.type}" role="alert">${state.sessionMessage.text}</p>`
    : "";

  return `
    <section class="panel sessions-panel" aria-labelledby="sessions-title">
      <div class="panel-heading">
        <div>
          <span class="tag">simulacion local</span>
          <h2 id="sessions-title">Sesiones</h2>
        </div>
        <a class="link-button" href="#/dashboard">Volver al dashboard</a>
      </div>

      <div class="section-box warning-box" role="note">
        <strong>Advertencia de multisesion simulada</strong>
        <p>Esta pantalla muestra una simulacion de politica de multisesion con datos ficticios. No entrega proteccion real contra secuestro de sesion, no usa IPs ni ubicaciones reales y no conecta servicios reales de ClaveUnica.</p>
      </div>

      <div class="summary-grid sessions-summary" aria-label="Resumen de sesiones simuladas">
        <div><span>Sesiones activas</span><strong>${activeSessions.length}</strong></div>
        <div><span>Sesion actual</span><strong>${escapeHtml(currentSession?.dispositivo || "No disponible")}</strong></div>
        <div><span>Persistencia</span><strong>solo estado demo/local</strong></div>
      </div>

      <div class="section-box">
        <div class="list-heading">
          <h3>Lista de sesiones activas</h3>
          <span class="tag">mock local</span>
        </div>
        ${message}
        <div class="sessions-list" aria-label="Lista de sesiones activas">
          ${sessions.map((item) => sessionCard(item)).join("")}
        </div>
      </div>
    </section>
  `;
}

function sessionCard(item) {
  const id = escapeHtml(item.id);
  const isClosed = item.estado === "cerrada demo";
  const risk = item.riesgo ? `<span class="risk-tag">${escapeHtml(item.riesgo)}</span>` : "";
  const currentTag = item.actual ? `<span class="tag">sesion actual</span>` : "";
  const action = item.actual
    ? `<button class="link-button" type="button" disabled>No cerrar aqui</button>`
    : `<button class="primary-button close-session-button" type="button" data-action="close-remote-session" data-session-id="${id}" ${isClosed ? "disabled" : ""}>${isClosed ? "Sesion cerrada" : "Cerrar sesion remota"}</button>`;

  return `
    <article class="session-card${item.actual ? " current-session" : ""}" aria-label="${item.actual ? "Sesion actual" : "Sesion remota simulada"}">
      <div class="session-card-header">
        <div>
          <h4>${escapeHtml(item.dispositivo)}</h4>
          <p>${escapeHtml(item.navegador)}</p>
        </div>
        <div class="session-tags">${currentTag}${risk}</div>
      </div>
      <dl class="session-details">
        <div><dt>Ubicacion</dt><dd>${escapeHtml(item.ubicacion)}</dd></div>
        <div><dt>Ultimo acceso</dt><dd>${escapeHtml(item.ultimoAcceso)}</dd></div>
        <div><dt>Estado</dt><dd>${escapeHtml(item.estado)}</dd></div>
      </dl>
      <div class="session-actions">${action}</div>
    </article>
  `;
}

function personalDataView() {
  const user = state.data.user;
  const nombre = escapeHtml(user.nombre);
  const run = escapeHtml(user.runEnmascarado || "12.345.***-*");
  const correo = escapeHtml(user.correo);
  const telefono = escapeHtml(user.telefono);
  const claveUnicaEstado = escapeHtml(user.claveUnicaEstado || "activa demo");
  const message = state.personalDataMessage
    ? `<p class="form-${state.personalDataMessage.type}" role="alert">${state.personalDataMessage.text}</p>`
    : "";

  return `
    <section class="panel personal-data-panel" aria-labelledby="personal-data-title">
      <div class="panel-heading">
        <div>
          <span class="tag">validacion simulada</span>
          <h2 id="personal-data-title">Datos personales</h2>
        </div>
        <a class="link-button" href="#/dashboard">Volver al dashboard</a>
      </div>

      <div class="personal-summary" aria-label="Datos personales simulados">
        <div><span>Nombre</span><strong>${nombre}</strong></div>
        <div><span>RUN</span><strong>${run}</strong></div>
        <div><span>Correo</span><strong>${correo}</strong></div>
        <div><span>Telefono</span><strong>${telefono}</strong></div>
        <div><span>ClaveUnica</span><strong>${claveUnicaEstado}</strong></div>
        <div><span>2FA</span><strong>${user.segundoFactorActivo ? "activo" : "inactivo"}</strong></div>
      </div>

      <form class="section-box personal-form" id="personal-data-form" autocomplete="off" novalidate>
        <div class="form-intro">
          <span class="tag">sin backend real</span>
          <p>Los cambios de correo y telefono son locales del prototipo. Antes de guardar se exige un factor de seguridad demo; no se usan servicios reales de ClaveUnica.</p>
        </div>
        <div class="personal-form-grid">
          <div class="form-field">
            <label for="personal-email">Editar correo electronico</label>
            <input id="personal-email" name="correo" type="email" value="${correo}" required>
          </div>
          <div class="form-field">
            <label for="personal-phone">Editar telefono</label>
            <input id="personal-phone" name="telefono" type="tel" value="${telefono}" required>
          </div>
          <div class="form-field security-factor-field">
            <label for="personal-security-code">Factor de seguridad simulado</label>
            <input id="personal-security-code" name="factor" type="text" inputmode="numeric" maxlength="6" placeholder="Codigo demo" required>
          </div>
        </div>
        ${message}
        <div class="form-actions">
          <button class="primary-button" type="submit">Guardar cambios</button>
          <button class="link-button" type="button" data-action="cancel-personal-data">Cancelar edicion</button>
        </div>
      </form>
    </section>
  `;
}

function validateLogin(form) {
  const auth = state.data.user.demoAuth || fallbackData.user.demoAuth;
  const usuario = form.usuario.value.trim();
  const clave = form.clave.value;

  if (usuario !== auth.usuario || clave !== auth.clave) {
    state.loginError = "Usuario o clave demo no válidos. Revisa las credenciales locales documentadas.";
    render();
    return;
  }

  state.loginError = "";
  if (state.data.user.segundoFactorActivo) {
    state.pendingUserId = state.data.user.id;
    sessionStorage.setItem("claveunica_demo_pending_user", state.pendingUserId);
    window.location.hash = "#/2fa-verificacion";
    return;
  }

  setPrivateMode(true);
}

function validateOtp(form) {
  const auth = state.data.user.demoAuth || fallbackData.user.demoAuth;
  const otp = form.otp.value.trim();

  if (otp !== auth.otp) {
    state.otpError = "Código OTP demo incorrecto. Usa el valor de prueba indicado en el README.";
    render();
    return;
  }

  setPrivateMode(true);
}

function validatePersonalData(form) {
  const security = state.data.user.personalSecurity || {};
  const expectedFactor = security.codigoDemo || state.data.user.demoAuth?.otp || fallbackData.user.demoAuth.otp;
  const correo = form.correo.value.trim();
  const telefono = form.telefono.value.trim();
  const factor = form.factor.value.trim();

  if (!correo || !telefono) {
    state.personalDataMessage = {
      type: "error",
      text: "Correo y telefono son obligatorios para guardar cambios demo."
    };
    render();
    return;
  }

  if (factor !== expectedFactor) {
    state.personalDataMessage = {
      type: "error",
      text: "Factor de seguridad incorrecto. No se guardaron cambios."
    };
    render();
    return;
  }

  state.data.user.correo = correo;
  state.data.user.telefono = telefono;
  state.personalDataMessage = {
    type: "success",
    text: "Datos personales actualizados localmente en el prototipo."
  };
  render();
}

function closeRemoteSession(sessionId) {
  const sessions = state.data.sessions || [];
  const session = sessions.find((item) => item.id === sessionId);

  if (!session) {
    state.sessionMessage = {
      type: "error",
      text: "No se encontro la sesion remota simulada."
    };
    render();
    return;
  }

  if (session.actual) {
    state.sessionMessage = {
      type: "error",
      text: "La sesion actual no se puede cerrar desde esta lista. Usa el boton general Cerrar sesion."
    };
    render();
    return;
  }

  session.estado = "cerrada demo";
  session.riesgo = "";
  state.data.user.sesionesActivas = sessions.filter((item) => item.estado === "activa").length;
  state.sessionMessage = {
    type: "success",
    text: "Sesion remota cerrada localmente en el prototipo."
  };
  render();
}

function completeDduConfiguration() {
  updateDduState({
    estado: "configurado",
    alertaPendiente: false,
    domicilio: "Domicilio Digital Unico configurado localmente en demo",
    fechaConfiguracion: "2026-07-05 12:00",
    canal: "Pasarela simulada DDU",
    casillaDemo: "DDU-LOCAL-001"
  });
  state.dduGatewayCancelConfirm = false;
  state.dduMessage = {
    type: "success",
    text: "Configuracion demo completada. Retorno al portal realizado; el dashboard mostrara DDU configurado."
  };
  window.location.hash = "#/ddu";
}

function openNotification(notificationId) {
  state.selectedNotificationId = notificationId;
  state.notificationMessage = null;
  render();
}

function backToNotificationList() {
  state.selectedNotificationId = "";
  state.notificationMessage = null;
  render();
}

function markNotificationRead(notificationId) {
  const notification = (state.data.notifications || []).find((item) => item.id === notificationId);

  if (!notification) {
    state.notificationMessage = {
      type: "error",
      text: "No se encontro la notificacion demo seleccionada."
    };
    render();
    return;
  }

  notification.estado = "leida demo";
  saveReadNotifications();
  state.notificationMessage = {
    type: "success",
    text: "Notificacion marcada como leida en estado local demo."
  };
  render();
}

function openAuthorization(authorizationId) {
  state.selectedAuthorizationId = authorizationId;
  state.authorizationMessage = null;
  render();
}

function backToAuthorizationList() {
  state.selectedAuthorizationId = "";
  state.authorizationMessage = null;
  render();
}

function applyAuthorizationDecision(authorizationId, decision, factor) {
  const authorization = (state.data.authorizations || []).find((item) => item.id === authorizationId);
  const expectedFactor = state.data.user.personalSecurity?.codigoDemo || state.data.user.demoAuth?.otp || fallbackData.user.demoAuth.otp;
  const nextByDecision = {
    aprobar: {
      allowed: "pendiente",
      estado: "aprobada",
      history: "aprobacion demo registrada localmente",
      success: "Autorizacion aprobada localmente en modo demo."
    },
    rechazar: {
      allowed: "pendiente",
      estado: "rechazada",
      history: "rechazo demo registrado localmente",
      success: "Autorizacion rechazada localmente en modo demo."
    },
    revocar: {
      allowed: "aprobada",
      estado: "revocada",
      history: "revocacion demo registrada localmente",
      success: "Autorizacion revocada localmente en modo demo."
    }
  };
  const config = nextByDecision[decision];

  if (!authorization || !config) {
    state.authorizationMessage = {
      type: "error",
      text: "No se encontro la autorizacion demo seleccionada."
    };
    render();
    return;
  }

  if (authorization.estado !== config.allowed) {
    state.authorizationMessage = {
      type: "error",
      text: "La autorizacion seleccionada esta en solo lectura para esta accion."
    };
    render();
    return;
  }

  if (factor !== expectedFactor) {
    state.authorizationMessage = {
      type: "error",
      text: "Factor demo obligatorio incorrecto. No se modifico la autorizacion."
    };
    render();
    return;
  }

  authorization.estado = config.estado;
  authorization.fechaDecision = "2026-07-05 12:30";
  authorization.historial = [
    ...(authorization.historial || []),
    `2026-07-05 12:30 ${config.history}`
  ];
  saveAuthorizationState();
  state.authorizationMessage = {
    type: "success",
    text: config.success
  };
  render();
}

function render() {
  const route = (window.location.hash || "#/inicio").replace("#/", "");
  const publicRoutes = ["inicio", "ayuda", "novedades"];
  const authRoutes = ["login", "2fa-verificacion"];

  if (route === "login") {
    app.innerHTML = loginView();
  } else if (route === "2fa-verificacion") {
    app.innerHTML = state.pendingUserId ? otpView() : loginView();
  } else if (!state.isPrivate && !publicRoutes.includes(route) && !authRoutes.includes(route)) {
    window.location.hash = "#/login";
    return;
  } else if (!state.isPrivate || publicRoutes.includes(route)) {
    app.innerHTML = route === "ayuda" || route === "novedades" ? publicInfo(route) : publicHome();
  } else {
    app.innerHTML = privateShell(route);
  }

  app.focus({ preventScroll: true });
}

document.addEventListener("click", (event) => {
  const action = event.target.closest("[data-action]")?.dataset.action;
  if (!action) return;

  if (action === "login") beginLogin();
  if (action === "logout") setPrivateMode(false);
  if (action === "activate") window.location.hash = "#/inicio";
  if (action === "recover") window.location.hash = "#/ayuda";
  if (action === "close-remote-session") {
    closeRemoteSession(event.target.closest("[data-session-id]")?.dataset.sessionId || "");
  }
  if (action === "open-ddu-confirmation") {
    state.dduModalOpen = true;
    state.dduMessage = null;
    render();
  }
  if (action === "cancel-ddu-modal") {
    state.dduModalOpen = false;
    state.dduMessage = {
      type: "error",
      text: "Configuracion DDU cancelada. El estado sigue pendiente/no configurado."
    };
    render();
  }
  if (action === "continue-ddu-gateway") {
    state.dduModalOpen = false;
    state.dduMessage = null;
    window.location.hash = "#/ddu-configuracion-demo";
  }
  if (action === "request-ddu-gateway-cancel") {
    state.dduGatewayCancelConfirm = true;
    render();
  }
  if (action === "keep-ddu-gateway") {
    state.dduGatewayCancelConfirm = false;
    render();
  }
  if (action === "confirm-ddu-gateway-cancel") {
    state.dduGatewayCancelConfirm = false;
    state.dduMessage = {
      type: "error",
      text: "Cancelacion confirmada en pasarela simulada. DDU permanece pendiente/no configurado."
    };
    window.location.hash = "#/ddu";
  }
  if (action === "cancel-personal-data") {
    state.personalDataMessage = null;
    render();
  }
  if (action === "open-notification") {
    openNotification(event.target.closest("[data-notification-id]")?.dataset.notificationId || "");
  }
  if (action === "back-notification-list") {
    backToNotificationList();
  }
  if (action === "mark-notification-read") {
    markNotificationRead(event.target.closest("[data-notification-id]")?.dataset.notificationId || "");
  }
  if (action === "open-authorization") {
    openAuthorization(event.target.closest("[data-authorization-id]")?.dataset.authorizationId || "");
  }
  if (action === "back-authorization-list") {
    backToAuthorizationList();
  }
});

document.addEventListener("submit", (event) => {
  if (event.target.id === "login-form") {
    event.preventDefault();
    validateLogin(event.target);
  }

  if (event.target.id === "otp-form") {
    event.preventDefault();
    validateOtp(event.target);
  }

  if (event.target.id === "personal-data-form") {
    event.preventDefault();
    validatePersonalData(event.target);
  }

  if (event.target.id === "ddu-gateway-form") {
    event.preventDefault();
    completeDduConfiguration();
  }

  if (event.target.id === "authorization-decision-form") {
    event.preventDefault();
    applyAuthorizationDecision(
      event.target.dataset.authorizationId || "",
      event.submitter?.dataset.authorizationDecision || "",
      event.target.factor.value.trim()
    );
  }
});

window.addEventListener("hashchange", render);

loadMocks().then(render);
