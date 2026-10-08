"use strict";

(() => {
  const data = JSON.parse(document.getElementById("catalog").textContent);
  const byId = (id) => document.getElementById(id);
  const tabs = [...document.querySelectorAll("[data-tab]")];
  const palette = { ...data.palette, "1": [255, 255, 255, 255] };
  const white = [255, 255, 255, 255];
  let grid = false;
  let motionFrame = 0;
  let motionRequest = null;
  let motionStart = 0;

  function node(tag, text, className) {
    const element = document.createElement(tag);
    if (text !== undefined) element.textContent = text;
    if (className) element.className = className;
    return element;
  }

  function color(rgba) { return `rgba(${rgba[0]},${rgba[1]},${rgba[2]},${rgba[3] / 255})`; }
  function hex(rgba) { return `#${rgba.slice(0, 3).map((value) => value.toString(16).padStart(2, "0")).join("").toUpperCase()}`; }

  function paint(canvas, rows, scale, cells = false, tint = null) {
    canvas.width = rows[0].length * scale;
    canvas.height = rows.length * scale;
    const context = canvas.getContext("2d");
    context.imageSmoothingEnabled = false;
    rows.forEach((row, y) => [...row].forEach((symbol, x) => {
      if (symbol === "." || symbol === "0" || symbol === " ") return;
      context.fillStyle = color(tint || palette[symbol] || white);
      context.fillRect(x * scale, y * scale, scale, scale);
    }));
    if (cells) {
      context.strokeStyle = "#34424d";
      context.lineWidth = 1;
      for (let x = 0; x <= canvas.width; x += scale) {
        context.beginPath(); context.moveTo(x + 0.5, 0); context.lineTo(x + 0.5, canvas.height); context.stroke();
      }
      for (let y = 0; y <= canvas.height; y += scale) {
        context.beginPath(); context.moveTo(0, y + 0.5); context.lineTo(canvas.width, y + 0.5); context.stroke();
      }
    }
  }

  function download(blob, name) {
    const url = URL.createObjectURL(blob);
    const link = node("a"); link.href = url; link.download = name; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function png(rows, name) {
    const canvas = node("canvas");
    paint(canvas, rows, data.cell_scale);
    canvas.toBlob((blob) => { if (blob) download(blob, `${name}.png`); });
  }

  function assetCard(item, scale, showGrid = false) {
    const rows = () => item.frames ? item.frames[motionFrame] : item.rows;
    const article = node("article", undefined, "asset-card");
    article.append(node("h3", item.name));
    article.append(node("div", `${item.rows[0].length} × ${item.rows.length} source cells${item.phase ? ` · ${item.phase} · WFF ${item.condition}` : ""}`, "card-meta"));
    const canvas = node("canvas"); canvas.setAttribute("aria-label", item.name);
    paint(canvas, rows(), scale, showGrid); article.append(canvas);
    const buttons = node("div", undefined, "download-row");
    const image = node("button", "PNG"); image.setAttribute("aria-label", `Download ${item.name} PNG`);
    image.addEventListener("click", () => png(rows(), `raster90-${item.id}${item.frames ? `-frame-${motionFrame + 1}` : ""}`));
    const matrix = node("button", "Matrix JSON"); matrix.setAttribute("aria-label", `Download ${item.name} matrix`);
    matrix.addEventListener("click", () => download(new Blob([JSON.stringify({ name: item.id, license: data.art_license, rows: rows(), ...(item.frames ? { frame_index: motionFrame, frame_rate: data.motion.fps } : {}) }, null, 2) + "\n"], { type: "application/json" }), `raster90-${item.id}.json`));
    buttons.append(image, matrix); article.append(buttons);
    const details = node("details"); details.append(node("summary", "Source cells"), node("pre", item.rows.join("\n"))); article.append(details);
    return article;
  }

  function activate(name) {
    if (!tabs.some((tab) => tab.dataset.tab === name)) name = "design";
    stopMotion();
    tabs.forEach((tab) => {
      const selected = tab.dataset.tab === name;
      tab.setAttribute("aria-selected", String(selected)); tab.tabIndex = selected ? 0 : -1;
      byId(`panel-${tab.dataset.tab}`).hidden = !selected;
    });
    if (name === "motion") setMotionFrame(0);
  }

  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => { history.replaceState(null, "", `#${tab.dataset.tab}`); activate(tab.dataset.tab); });
    tab.addEventListener("keydown", (event) => {
      const key = event.key;
      if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(key)) return;
      event.preventDefault();
      const next = key === "Home" ? 0 : key === "End" ? tabs.length - 1 : (index + (key === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length;
      tabs[next].click(); tabs[next].focus();
    });
  });
  window.addEventListener("hashchange", () => activate(location.hash.slice(1)));

  const paletteNames = { W: "White / base", Y: "Yellow / sun", C: "Cyan / night", B: "Blue / weather" };
  Object.entries(data.palette).forEach(([symbol, rgba]) => {
    const card = node("article", undefined, "swatch");
    const strip = node("div", undefined, "swatch-color"); strip.style.setProperty("--swatch", hex(rgba));
    card.append(strip, node("h3", paletteNames[symbol] || symbol), node("p", hex(rgba))); byId("palette").append(card);
  });

  Object.entries(data.fonts).forEach(([key, font]) => {
    const option = node("option", font.label); option.value = key; byId("font-cut").append(option);
  });

  function renderFont() {
    const key = byId("font-cut").value;
    const font = data.fonts[key];
    const scale = Number(byId("font-scale").value);
    const lines = byId("sample").value.split("\n");
    const missing = [...new Set([...lines.join("")].filter((character) => !font.glyphs[character]))];
    byId("unsupported").textContent = missing.length ? `Outside this cut (skipped): ${missing.join(" ")}` : "";
    byId("font-role").textContent = font.role;
    const height = Object.values(font.glyphs)[0].length;
    const widths = lines.map((line) => [...line].reduce((sum, character) => sum + (font.glyphs[character] ? font.glyphs[character][0].length + 1 : 0), 0));
    const canvas = byId("font-preview");
    canvas.width = Math.max(1, ...widths) * scale + 6 * scale;
    canvas.height = lines.length * (height + 2) * scale + 6 * scale;
    const context = canvas.getContext("2d"); context.fillStyle = "white";
    lines.forEach((line, lineIndex) => {
      let x = 3 * scale;
      const y = (3 + lineIndex * (height + 2)) * scale;
      [...line].forEach((character) => {
        const rows = font.glyphs[character]; if (!rows) return;
        rows.forEach((row, rowIndex) => [...row].forEach((cell, column) => {
          if (cell === "1") context.fillRect(x + column * scale, y + rowIndex * scale, scale, scale);
        }));
        x += (rows[0].length + 1) * scale;
      });
    });
    byId("glyphs").replaceChildren();
    byId("glyph-summary").textContent = `Browse ${Object.keys(font.glyphs).length} glyphs`;
    Object.entries(font.glyphs).forEach(([character, rows]) => {
      const card = node("article", undefined, "glyph-card");
      const glyph = node("canvas"); glyph.setAttribute("aria-label", `Glyph ${character === " " ? "space" : character}`);
      paint(glyph, rows, 3);
      const included = key === "clean" || (key === "compact" && data.runtime_compact_keys.includes(character));
      card.append(node("span", character === " " ? "SPACE" : character), glyph, node("span", included ? "WFF subset" : "Source vocabulary", "card-meta"));
      byId("glyphs").append(card);
    });
  }
  ["font-cut", "font-scale", "sample"].forEach((id) => byId(id).addEventListener("input", renderFont));
  byId("font-download").addEventListener("click", () => byId("font-preview").toBlob((blob) => { if (blob) download(blob, "raster90-text-sample.png"); }));

  function renderIcons() {
    const scale = Number(byId("icon-scale").value);
    const query = byId("icon-search").value.trim().toLowerCase();
    const phase = byId("icon-phase").value;
    const matches = data.weather.filter((item) => (phase === "both" || phase === item.phase) && item.name.includes(query));
    byId("weather-icons").replaceChildren(...matches.map((item) => assetCard(item, scale, grid)));
    byId("utility-icons").replaceChildren(...data.utility.map((item) => assetCard(item, scale, grid)));
    byId("icon-count").textContent = `${matches.length} / ${data.weather.length} day/night mappings`;
  }
  ["icon-search", "icon-phase", "icon-scale"].forEach((id) => byId(id).addEventListener("input", renderIcons));
  byId("icon-grid").addEventListener("click", () => { grid = !grid; byId("icon-grid").setAttribute("aria-pressed", String(grid)); renderIcons(); });
  const battery = data.utility.find((item) => item.id === "battery");
  data.battery_bands.forEach((band) => {
    const figure = node("figure"); const canvas = node("canvas"); paint(canvas, battery.rows, 3, false, band.rgba);
    const range = band.minimum_exclusive === null ? `0–${band.maximum_inclusive}%` : band.maximum_inclusive === null ? `>${band.minimum_exclusive}%` : `>${band.minimum_exclusive}–${band.maximum_inclusive}%`;
    figure.append(canvas, node("figcaption", `${band.name} · ${range}`)); byId("battery-bands").append(figure);
  });

  const motionCanvases = [];
  Object.entries(data.motion.families).forEach(([name, frames]) => {
    const item = { id: name, name: name.replaceAll("_", " "), rows: frames[0], frames };
    const card = assetCard(item, Number(byId("motion-scale").value));
    motionCanvases.push({ canvas: card.querySelector("canvas"), pre: card.querySelector("pre"), frames }); byId("motion-icons").append(card);
  });

  function setMotionFrame(frame) {
    motionFrame = frame;
    byId("motion-frame").value = String(frame);
    byId("motion-position").textContent = `${frame + 1} / ${data.motion.frames}`;
    motionCanvases.forEach(({ canvas, pre, frames }) => {
      paint(canvas, frames[frame], Number(byId("motion-scale").value));
      pre.textContent = frames[frame].join("\n");
    });
  }

  function stopMotion() {
    if (motionRequest !== null) cancelAnimationFrame(motionRequest);
    motionRequest = null; byId("motion-play").textContent = "Play once";
  }

  function tick(now) {
    const frame = Math.floor((now - motionStart) * data.motion.fps / 1000);
    if (frame >= data.motion.frames) { stopMotion(); setMotionFrame(0); return; }
    if (frame !== motionFrame) setMotionFrame(frame);
    motionRequest = requestAnimationFrame(tick);
  }
  byId("motion-play").addEventListener("click", () => {
    if (motionRequest !== null) { stopMotion(); return; }
    setMotionFrame(0); motionStart = performance.now(); byId("motion-play").textContent = "Pause";
    motionRequest = requestAnimationFrame(tick);
  });
  byId("motion-reset").addEventListener("click", () => { stopMotion(); setMotionFrame(0); });
  byId("motion-frame").addEventListener("input", () => { stopMotion(); setMotionFrame(Number(byId("motion-frame").value)); });
  byId("motion-scale").addEventListener("input", () => setMotionFrame(motionFrame));
  document.addEventListener("visibilitychange", () => { if (document.hidden) { stopMotion(); setMotionFrame(0); } });

  data.captures.forEach((capture) => {
    const card = node("article", undefined, "capture-card");
    const image = node("img"); image.src = capture.url; image.alt = `${capture.target}, ${capture.mode}, ${capture.date}`; image.width = capture.width; image.height = capture.height; image.loading = "lazy";
    const record = node("a", "Checkpoint ↗"); record.href = capture.record_url;
    const details = node("details"); details.append(node("summary", "Exact capture hash"), node("code", capture.sha256));
    card.append(node("h3", capture.target), node("p", `${capture.date} · ${capture.kind} · ${capture.mode}`), image, node("p", capture.claim), record, details);
    byId("captures").append(card);
  });
  data.sources.forEach((source, index) => {
    if (index) byId("source-links").append(document.createTextNode(" · "));
    const link = node("a", source.path.startsWith("fonts") ? "Type matrices" : source.path.endsWith("animation.py") ? "Motion matrices" : "Icon matrices");
    link.href = source.url; byId("source-links").append(link);
  });
  renderFont(); renderIcons(); setMotionFrame(0); activate(location.hash.slice(1));
})();
