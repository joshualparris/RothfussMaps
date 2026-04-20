(function () {
  const data = window.UNIVERSITY_ATLAS_DATA;

  if (!data) {
    document.body.innerHTML = "<main style='padding:2rem;font-family:Palatino,serif'>Atlas data could not be loaded.</main>";
    return;
  }

  const state = {
    search: "",
    areaId: null,
    itemId: null,
    imageIndex: 0,
  };

  const els = {
    nav: document.getElementById("district-nav"),
    search: document.getElementById("atlas-search"),
    heroDistrict: document.getElementById("hero-district"),
    heroTitle: document.getElementById("hero-title"),
    heroBlurb: document.getElementById("hero-blurb"),
    heroRenderCount: document.getElementById("hero-render-count"),
    heroStatus: document.getElementById("hero-status"),
    areaLinks: document.getElementById("area-links"),
    canonNote: document.getElementById("canon-note"),
    studyCount: document.getElementById("study-count"),
    studyRail: document.getElementById("study-rail"),
    itemKind: document.getElementById("item-kind"),
    itemTitle: document.getElementById("item-title"),
    itemNote: document.getElementById("item-note"),
    cautionWrap: document.getElementById("item-caution-wrap"),
    imageStage: document.getElementById("image-stage"),
    thumbStrip: document.getElementById("thumb-strip"),
    imageCaption: document.getElementById("image-caption"),
    studyDetails: document.getElementById("study-details"),
    prevImage: document.getElementById("prev-image"),
    nextImage: document.getElementById("next-image"),
  };

  const districts = [...data.districts].sort((a, b) => a.order - b.order);
  const areas = [...data.areas].sort((a, b) => a.order - b.order);

  function areaById(id) {
    return areas.find((area) => area.id === id) || null;
  }

  function itemById(area, itemId) {
    return area?.items.find((item) => item.id === itemId) || null;
  }

  function encodePath(path) {
    return encodeURI(path).replace(/#/g, "%23");
  }

  function prettyKind(kind) {
    return {
      overview: "Overview",
      level: "Level Study",
      room: "Room Study",
      roof: "Roof Study",
      network: "Network Study",
      legacy: "Legacy Branch",
      reconstructed: "High Reconstruction",
    }[kind] || "Study";
  }

  function readHash() {
    const raw = location.hash.replace(/^#/, "");
    if (!raw) return null;
    const [areaId, itemId] = raw.split("/");
    return { areaId, itemId };
  }

  function writeHash() {
    const parts = [state.areaId];
    if (state.itemId) parts.push(state.itemId);
    history.replaceState(null, "", "#" + parts.filter(Boolean).join("/"));
  }

  function firstVisibleArea() {
    const needle = state.search.trim().toLowerCase();
    if (!needle) return areas[0];
    return areas.find((area) => {
      const bag = [
        area.title,
        area.blurb,
        area.canonNote,
        ...area.items.map((item) => `${item.title} ${item.note} ${item.caution}`),
      ].join(" ").toLowerCase();
      return bag.includes(needle);
    }) || areas[0];
  }

  function firstUsableItem(area) {
    return area.items[0] || null;
  }

  function renderNav() {
    const needle = state.search.trim().toLowerCase();
    els.nav.innerHTML = "";

    districts.forEach((district) => {
      const districtAreas = areas.filter((area) => area.district === district.id).filter((area) => {
        if (!needle) return true;
        const bag = [
          area.title,
          area.blurb,
          area.canonNote,
          ...area.items.map((item) => `${item.title} ${item.note} ${item.caution}`),
        ].join(" ").toLowerCase();
        return bag.includes(needle);
      });

      if (!districtAreas.length) return;

      const group = document.createElement("section");
      group.className = "district-group";
      group.innerHTML = `
        <h3>${district.name}</h3>
        <p class="district-motto">${district.motto}</p>
        <div class="area-list"></div>
      `;

      const areaList = group.querySelector(".area-list");

      districtAreas.forEach((area) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "area-btn" + (area.id === state.areaId ? " active" : "");
        btn.innerHTML = `
          <div class="area-btn-topline">
            <span class="area-title">${area.title}</span>
            <span class="status-pill">
              <span class="status-dot ${area.status}"></span>
              ${area.status === "rendered" ? "live" : "queued"}
            </span>
          </div>
          <div class="area-subline">
            <span>${area.renderCount} render${area.renderCount === 1 ? "" : "s"}</span>
            <span>${area.items.length} studies</span>
          </div>
        `;
        btn.addEventListener("click", () => {
          state.areaId = area.id;
          state.itemId = firstUsableItem(area)?.id || null;
          state.imageIndex = 0;
          writeHash();
          render();
        });
        areaList.appendChild(btn);
      });

      els.nav.appendChild(group);
    });
  }

  function renderHero(area) {
    els.heroDistrict.textContent = area.districtName;
    els.heroTitle.textContent = area.title;
    els.heroBlurb.textContent = area.blurb;
    els.heroRenderCount.textContent = String(area.renderCount);
    els.heroStatus.textContent = area.status === "rendered" ? "Active render set" : "Awaiting first render";

    els.areaLinks.innerHTML = "";
    area.links.forEach((link) => {
      const a = document.createElement("a");
      a.className = "link-chip";
      a.href = encodePath(link.path);
      a.textContent = link.label;
      a.target = "_blank";
      a.rel = "noreferrer";
      els.areaLinks.appendChild(a);
    });

    els.canonNote.textContent = area.canonNote;
  }

  function renderStudies(area) {
    els.studyRail.innerHTML = "";
    els.studyCount.textContent = `${area.items.length} study${area.items.length === 1 ? "" : "ies"} in this area`;

    if (!area.items.length) {
      const card = document.createElement("div");
      card.className = "study-card active";
      card.innerHTML = `
        <div class="study-topline">
          <span class="badge">queued</span>
        </div>
        <h4>Awaiting first render</h4>
        <p class="study-note">This area has prompt and brief links ready, but no exported image studies in this zip yet.</p>
      `;
      els.studyRail.appendChild(card);
      return;
    }

    area.items.forEach((item) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "study-card" + (item.id === state.itemId ? " active" : "");
      btn.innerHTML = `
        <div class="study-topline">
          <span class="badge">${item.badge}</span>
          ${item.caution ? `<span class="caution-pill">${item.caution}</span>` : ""}
        </div>
        <h4>${item.title}</h4>
        <p class="study-note">${item.note || "No extra note recorded for this study yet."}</p>
        <div class="study-footline">
          <span class="muted">${item.imageCount} image${item.imageCount === 1 ? "" : "s"}</span>
          <span class="muted">${item.docs.length} doc${item.docs.length === 1 ? "" : "s"}</span>
        </div>
      `;
      btn.addEventListener("click", () => {
        state.itemId = item.id;
        state.imageIndex = 0;
        writeHash();
        renderItem(area, item);
        renderStudies(area);
      });
      els.studyRail.appendChild(btn);
    });
  }

  function renderDetails(item) {
    if (!item) {
      els.studyDetails.innerHTML = "<p>Select a study to see its render list and supporting docs.</p>";
      return;
    }

    const imageList = item.images.length
      ? `
        <p><strong>Render files</strong></p>
        <ul class="image-list">
          ${item.images.map((image) => `<li><a href="${encodePath(image.path)}" target="_blank" rel="noreferrer">${image.name}</a></li>`).join("")}
        </ul>
      `
      : "<p>No images stored for this study yet.</p>";

    const docs = item.docs.length
      ? `
        <div class="details-links">
          ${item.docs.map((doc) => `<a href="${encodePath(doc.path)}" target="_blank" rel="noreferrer">${doc.name}</a>`).join("")}
        </div>
      `
      : "<p>No companion docs stored inside this study folder.</p>";

    els.studyDetails.innerHTML = `
      <p><strong>${item.title}</strong></p>
      <p>${item.note || "No special note recorded."}</p>
      ${item.caution ? `<p><strong>Caution:</strong> ${item.caution}.</p>` : ""}
      ${imageList}
      <p><strong>Companion docs</strong></p>
      ${docs}
    `;
  }

  function renderImage(item) {
    els.thumbStrip.innerHTML = "";
    els.imageCaption.innerHTML = "";

    if (!item || !item.images.length) {
      els.imageStage.className = "image-stage empty";
      els.imageStage.innerHTML = `
        <div class="empty-state">
          <p class="empty-title">No image in this study yet</p>
          <p class="empty-copy">The study card remains here so your build order stays honest. Use the linked prompts and docs to produce the next render.</p>
        </div>
      `;
      return;
    }

    state.imageIndex = Math.max(0, Math.min(state.imageIndex, item.images.length - 1));
    const current = item.images[state.imageIndex];

    els.imageStage.className = "image-stage";
    els.imageStage.innerHTML = "";
    const img = document.createElement("img");
    img.src = encodePath(current.path);
    img.alt = `${item.title} - ${current.name}`;
    els.imageStage.appendChild(img);

    item.images.forEach((image, index) => {
      const thumb = document.createElement("button");
      thumb.type = "button";
      thumb.className = "thumb-btn" + (index === state.imageIndex ? " active" : "");
      const thumbImg = document.createElement("img");
      thumbImg.src = encodePath(image.path);
      thumbImg.alt = image.name;
      thumb.appendChild(thumbImg);
      thumb.addEventListener("click", () => {
        state.imageIndex = index;
        renderImage(item);
      });
      els.thumbStrip.appendChild(thumb);
    });

    els.imageCaption.innerHTML = `
      <strong>${current.name}</strong><br>
      <span class="muted">${current.path}</span>
    `;
  }

  function renderItem(area, item) {
    els.itemKind.textContent = item ? prettyKind(item.kind) : "No study selected";
    els.itemTitle.textContent = item ? item.title : "Select a study";
    els.itemNote.textContent = item ? (item.note || "No extra note recorded.") : "Pick a study card to load its images, docs, and cautions.";
    els.cautionWrap.innerHTML = item?.caution ? `<span class="caution-pill">${item.caution}</span>` : "";
    renderImage(item);
    renderDetails(item);
  }

  function render() {
    const area = areaById(state.areaId) || firstVisibleArea();
    state.areaId = area.id;

    if (!state.itemId || !itemById(area, state.itemId)) {
      state.itemId = firstUsableItem(area)?.id || null;
      state.imageIndex = 0;
    }

    renderNav();
    renderHero(area);
    renderStudies(area);
    renderItem(area, itemById(area, state.itemId));
  }

  els.search.addEventListener("input", (event) => {
    state.search = event.target.value || "";
    const currentArea = areaById(state.areaId);
    const needle = state.search.trim().toLowerCase();
    if (needle) {
      const areaStillVisible = currentArea && [currentArea.title, currentArea.blurb, currentArea.canonNote, ...currentArea.items.map((item) => `${item.title} ${item.note} ${item.caution}`)].join(" ").toLowerCase().includes(needle);
      if (!areaStillVisible) {
        state.areaId = firstVisibleArea().id;
        state.itemId = firstUsableItem(areaById(state.areaId))?.id || null;
        state.imageIndex = 0;
      }
    }
    render();
  });

  els.prevImage.addEventListener("click", () => {
    const area = areaById(state.areaId);
    const item = itemById(area, state.itemId);
    if (!item?.images.length) return;
    state.imageIndex = (state.imageIndex - 1 + item.images.length) % item.images.length;
    renderImage(item);
  });

  els.nextImage.addEventListener("click", () => {
    const area = areaById(state.areaId);
    const item = itemById(area, state.itemId);
    if (!item?.images.length) return;
    state.imageIndex = (state.imageIndex + 1) % item.images.length;
    renderImage(item);
  });

  window.addEventListener("hashchange", () => {
    const hash = readHash();
    if (!hash) return;
    state.areaId = hash.areaId || state.areaId;
    state.itemId = hash.itemId || null;
    state.imageIndex = 0;
    render();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft") {
      els.prevImage.click();
    }
    if (event.key === "ArrowRight") {
      els.nextImage.click();
    }
  });

  const hash = readHash();
  if (hash) {
    state.areaId = hash.areaId || null;
    state.itemId = hash.itemId || null;
  }

  render();
})();
