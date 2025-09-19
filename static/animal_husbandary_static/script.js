document.addEventListener('DOMContentLoaded', () => {
  // Update year in footer
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Improve click area and keyboard support (anchors already focusable)
  const cards = document.querySelectorAll('.card');
  cards.forEach((card) => {
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        card.click();
      }
    });
  });

  // Navbar dropdown toggle (accessible)
  const dropdown = document.querySelector('.dropdown');
  const toggle = document.querySelector('.dropdown-toggle');
  const menu = document.querySelector('.dropdown-menu');
  if (dropdown && toggle && menu) {
    function closeMenu() {
      menu.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    }
    function openMenu() {
      menu.classList.add('open');
      toggle.setAttribute('aria-expanded', 'true');
    }
    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      if (menu.classList.contains('open')) closeMenu(); else openMenu();
    });
    document.addEventListener('click', (e) => {
      if (!dropdown.contains(e.target)) closeMenu();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeMenu();
    });
  }

  // Highlight active nav item
  const path = location.pathname.replace(/\\/g, '/');
  document.querySelectorAll('.dropdown-menu a, .nav > a').forEach((link) => {
    const href = link.getAttribute('href');
    if (!href) return;
    const isActive = path.endsWith('/' + href) || path.includes('/pages/') && href.includes(path.split('/').pop());
    if (isActive) link.style.fontWeight = '700';
  });

  // Richer, sectioned breed/species data per page
  const breedsData = {
    dairy: {
      'Gir Cow': {
        info: 'The Gir cow is one of the most prominent indigenous dairy breeds from Gujarat, India. It is known for its distinctive convex forehead, long ears, and docile temperament. Gir cows are highly resistant to tropical diseases and heat stress, making them an excellent choice for sustainable dairy farming in warm climates. Milk yield ranges between 1,200–1,800 liters per lactation with high fat content (4–5%).',
  food: 'The Gir cow thrives on locally available fodder. Main feed includes hybrid Napier grass, sorghum, maize, and seasonal green fodder like berseem and lucerne. Dry fodder such as wheat or rice straw should be mixed in daily rations. During lactation, concentrate feed rich in energy and protein is provided in proportion to milk yield (1kg concentrate per 2.5 liters milk). Mineral mixture and common salt are essential to maintain fertility and milk quality. Unlimited access to clean drinking water is crucial.',
  care: 'Daily grooming with a soft brush keeps the coat clean and improves circulation. Bathing during summer reduces heat stress. Hooves should be trimmed every 2–3 months to prevent lameness. Follow a regular deworming and tick-control schedule. Provide fly repellents during rainy season. Cows should be observed closely during calving to prevent birth complications. Calves must receive colostrum within the first 3 hours after birth for immunity.',
  environment: 'The breed adapts well to village-level housing. A shed with good ventilation, slope for drainage, and at least 3.5–4 sq. meters space per animal is ideal. Roof height of 10–12 feet ensures airflow. Floors should be non-slippery, dry, and easy to clean. Shade trees in paddocks reduce heat load. In colder regions, use curtains or bedding to protect from cold winds.',
  diseases: 'Major threats include mastitis, foot-and-mouth disease (FMD), hemorrhagic septicemia (HS), parasitic infestations, and heat stress. Nutritional deficiencies can lead to infertility and metabolic disorders. Watch for signs such as sudden drop in appetite, dullness, udder swelling, fever, limping, or abnormal milk.',
  treatment: 'Preventive vaccination is critical: FMD twice yearly, HS annually, and Brucellosis as per schedule. Sanitize milking equipment and use post-milking teat dips to avoid mastitis. For internal parasites, follow deworming every 3–4 months. Isolate sick animals immediately. Provide oral rehydration and supportive care until veterinary treatment is available.',
        image: 'static/assets/animal_husbandary/gir_cow.png'
      },
      'Murrah Buffalo': {
        info: 'Murrah is a renowned buffalo breed from Haryana that gives rich, high-fat milk. It performs well across regions when housing, feeding, and hygiene are maintained. With proper management, Murrah buffaloes can sustain steady yields throughout lactation.',
        food: 'Offer green fodder like hybrid Napier, maize, and berseem along with quality dry roughage. During peak milk, increase energy by adding balanced concentrates according to yield. Provide mineral mixture and a salt lick, and ensure constant access to plenty of clean water.',
        care: 'Buffaloes love water; provide a wallow tank or hose down twice daily in hot months to reduce heat stress. Keep udders clean before and after milking and practice teat dipping. Follow deworming and vaccination schedules and trim horns if necessary for handler safety.',
        environment: 'Provide cool, shaded housing with good ventilation and non-slippery floors. Maintain drainage to keep pens dry and control flies and mosquitoes. Separate feeding and resting areas to reduce stress and fighting within the herd.',
        diseases: 'Mastitis, hemorrhagic septicemia (HS), and internal/external parasites are common risks. Heat stress and foot issues occur on wet, slippery floors. Look for clots in milk, fever, swollen quarters, or lameness as warning signs.',
        treatment: 'Vaccinate on schedule for HS and FMD and maintain strict milking hygiene. Use teat dipping after every milking and keep bedding clean and dry. Seek veterinary help promptly for antibiotics and supportive care when disease is suspected.',
        image: 'static/assets/animal_husbandary/murrah_buffalo.png'
      },
      'Holstein Friesian': {
        info: 'Very high-yield exotic breed; needs better management.',
        food: 'High energy ration, balanced protein, minerals; constant clean water.',
        care: 'Strict milking hygiene; watch for metabolic disorders.',
        environment: 'Cool, clean shed; fans/misting in hot areas.',
        diseases: 'Mastitis, milk fever, ketosis.',
        treatment: 'Prevent with balanced diet and minerals; call vet promptly.',
        image: 'static/assets/animal_husbandary/holstein_friesian.png'
      },
      'Jersey': {
        info: 'Smaller framed, high milk fat; adaptable to many climates.',
        food: 'Quality fodder with mineral mix; do not overfeed concentrates.',
        care: 'Gentle handling; regular vaccination and deworming.',
        environment: 'Dry floors, good airflow; shade in summer.',
        diseases: 'Mastitis, parasites.',
        treatment: 'Milking hygiene, teat dipping, deworming schedule.',
        image: 'static/assets/animal_husbandary/jersey_cow.png'
      }
    },
    poultry: {
      'Aseel': {
        info: 'Native chicken known for hardiness and meat quality.',
        food: 'Balanced grower/finisher feed; clean water; calcium for layers.',
        care: 'Keep litter dry; trim beaks if pecking; maintain biosecurity.',
        environment: 'Well-ventilated shed; avoid overcrowding; proper lighting.',
        diseases: 'ND (Ranikhet), coccidiosis, respiratory issues.',
        treatment: 'Vaccination schedule, coccidiostats as advised, isolate sick birds.',
        image: 'static/assets/animal_husbandary/aseel_chicken.png'
      },
      'Kadaknath': {
        info: 'Black meat native breed with good market demand.',
        food: 'Quality layer/broiler feed as per purpose; greens as supplement.',
        care: 'Clean waterers daily; control external parasites.',
        environment: 'Dry litter, moderate temperature, protect from predators.',
        diseases: 'Fowl pox, ectoparasites, coccidiosis.',
        treatment: 'Vaccinate, maintain hygiene, use approved dewormers/antiparasitics.',
        image: 'static/assets/animal_husbandary/kadaknath.png'
      },
      'White Leghorn': {
        info: 'Efficient layer breed, early maturity and high egg output.',
        food: 'Layer feed with adequate calcium and vitamins.',
        care: 'Regular egg collection; maintain shell quality with minerals.',
        environment: 'Good airflow; controlled lighting for laying cycles.',
        diseases: 'Egg drop syndrome, respiratory diseases.',
        treatment: 'Biosecurity, vaccination, vet-guided medications.',
        image: 'static/assets/animal_husbandary/white_leghorn.png'
      }
    },
    pisciculture: {
      'Rohu (Labeo rohita)': {
        info: 'Major carp favored for taste and growth in ponds.',
        food: 'Balanced pelleted feed; natural pond plankton; avoid overfeeding.',
        care: 'Regular sampling and grading; maintain dissolved oxygen.',
        environment: 'Clean pond with proper liming and fertilization.',
        diseases: 'EUS, gill infections, parasitic infestations.',
        treatment: 'Lime and salt as advised, improve water quality, consult fisheries expert.',
        image: 'static/assets/animal_husbandary/rohu_fish.png'
      },
      'Catla (Catla catla)': {
        info: 'Surface-feeding carp commonly stocked with Rohu and Mrigal.',
        food: 'Floating pellets; maintain feeding trays/points.',
        care: 'Avoid sudden temperature or pH changes; aerate when needed.',
        environment: 'Well-prepared pond; avoid overcrowding.',
        diseases: 'Gill flukes, bacterial infections.',
        treatment: 'Prophylactic baths, maintain water quality, expert advice.',
        image: 'static/assets/animal_husbandary/catla_fish.png'
      },
      'Tilapia': {
        info: 'Fast growing and hardy; control breeding to prevent overcrowding.',
        food: 'Commercial pellets; supplement with natural feed; steady schedule.',
        care: 'Grade fish periodically; ensure good oxygen levels.',
        environment: 'Temperature-friendly waters; adequate biosecurity at inlets.',
        diseases: 'Streptococcosis, parasites.',
        treatment: 'Quarantine seed, maintain water quality, vet-approved treatments.',
        image: 'static/assets/animal_husbandary/tilapia.png'
      }
    },
    apiculture: {
      'Indian Hive Bee (Apis cerana indica)': {
        info: 'Indian honey bee adapted to tropical climates; manageable colonies.',
        food: 'Natural nectar and pollen; sugar feeding in dearth periods.',
        care: 'Regular inspections; avoid crushing bees; keep brood healthy.',
        environment: 'Hives in shaded, calm areas near flowers and water.',
        diseases: 'Varroa mites, wax moths, foulbrood.',
        treatment: 'Good hive hygiene, managed brood breaks, approved mite control.',
        image: 'static/assets/animal_husbandary/indian_hive_bee.png'
      },
      'Rock Bee (Apis dorsata)': {
        info: 'Wild rock bee species forming large open combs; not domesticated for hives.',
        food: 'Nectar and pollen from wild flora; no feeding needed.',
        care: 'Not reared in boxes; information for awareness and safety.',
        environment: 'Cliffs, tall trees, and buildings in warm regions.',
        diseases: 'Wild species face predators and parasites.',
        treatment: 'Not applicable; avoid disturbing colonies; seek experts for removal.',
        image: 'static/assets/animal_husbandary/rock_bee.png'
      }
    },
    sericulture: {
      'Mulberry Silkworm (Bombyx mori)': {
        info: 'Primary domesticated silkworm species reared on mulberry leaves.',
        food: 'Fresh mulberry leaves sorted by instar stage; clean and pest-free.',
        care: 'Gentle handling; regular bed cleaning; proper spacing by instar.',
        environment: 'Controlled temperature and humidity per instar; good ventilation.',
        diseases: 'Grasserie, pébrine, muscardine.',
        treatment: 'Disinfect rearing rooms; use lime/bleach as advised; disease-free layings.',
        image: 'static/assets/animal_husbandary/mulberry_silkworm.png'
      },
      'Tasar Silkworm (Antheraea mylitta)': {
        info: 'Wild silkworm species producing tasar silk; reared outdoors on host trees.',
        food: 'Leaves of Terminalia and other host trees; free from sprays.',
        care: 'Protect from predators; monitor weather; handle gently during mounting.',
        environment: 'Outdoor rearing on host plants in suitable regions.',
        diseases: 'Predation, parasitism, and weather-related losses.',
        treatment: 'Field hygiene, predator nets, expert guidance for disease control.',
        image: 'static/assets/animal_husbandary/tasar_silkworm.png'
      }
    }
  };

  const pageSection = document.querySelector('section.content[data-page]');
  if (pageSection) {
    const pageKey = pageSection.getAttribute('data-page');
    const selectEl = pageSection.querySelector('.breed-select');
    const gridEl = pageSection.querySelector('.breed-grid');
    const gridBtn = pageSection.querySelector('.breed-grid-button');
    const detailsEl = pageSection.querySelector('.breed-details');
    const itemsObj = breedsData[pageKey] || {};
    const names = Object.keys(itemsObj);

    // Populate select
    if (selectEl) {
      selectEl.innerHTML = '<option value="">Select a breed/species…</option>' +
        names.map((n) => `<option value="${n}">${n}</option>`).join('');
      selectEl.addEventListener('change', (e) => {
        const key = e.target.value;
        if (key && itemsObj[key]) {
          location.href = `/animal_husbandary_pages/breed.html?type=${encodeURIComponent(pageKey)}&name=${encodeURIComponent(key)}`;
        }
      });
    }

    // Populate grid
    function populateGrid() {
      if (!gridEl) return;
      gridEl.innerHTML = names.map((name) => {
        const b = itemsObj[name];
        const src = b && b.image ? ('../' + b.image) : '';
        const alt = name;
        return `
        <div class="breed-item" data-name="${name}" tabindex="0">
          ${src ? `<img class="breed-photo" src="${src}" alt="${alt}" onload="this.classList.add('is-ready')" />` : ''}
          <strong>${name}</strong>
        </div>`;
      }).join('');
      gridEl.querySelectorAll('.breed-item').forEach((el) => {
        el.addEventListener('click', () => {
          const name = el.getAttribute('data-name');
          if (name && itemsObj[name]) {
            location.href = `/animal_husbandary_pages/breed.html?type=${encodeURIComponent(pageKey)}&name=${encodeURIComponent(name)}`;
          }
        });
        el.addEventListener('keydown', (e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            el.click();
          }
        });
      });
    }

    if (gridBtn && gridEl) {
      gridBtn.addEventListener('click', () => {
        const nowHidden = !gridEl.hasAttribute('hidden');
        if (nowHidden) {
          gridEl.setAttribute('hidden', '');
          gridBtn.textContent = 'Browse as Grid';
        } else {
          populateGrid();
          gridEl.removeAttribute('hidden');
          gridBtn.textContent = 'Hide Grid';
        }
      });
    }

    function renderDetails(name, b) {
      if (!detailsEl || !b) return;
      detailsEl.innerHTML = `
        <div class="breed-header">
          <img class="breed-photo" src="${'../' + b.image}" alt="${name}" />
          <div>
            <h3 style="margin: 0 0 2px; font-size: 20px;">${name}</h3>
            <p style="margin: 0; color: var(--muted);">Quick information and best practices</p>
          </div>
        </div>
        <div class="accordion">
          <details class="accordion-details accordion-item" open>
            <summary class="accordion-summary"><span class="emoji">📘</span> General Information</summary>
            <div class="accordion-content">${b.info || '—'}</div>
          </details>
          <details class="accordion-details accordion-item">
            <summary class="accordion-summary"><span class="emoji">🥕</span> Food and Nutrition</summary>
            <div class="accordion-content">${b.food || '—'}</div>
          </details>
          <details class="accordion-details accordion-item">
            <summary class="accordion-summary"><span class="emoji">🧼</span> Care</summary>
            <div class="accordion-content">${b.care || '—'}</div>
          </details>
          <details class="accordion-details accordion-item">
            <summary class="accordion-summary"><span class="emoji">🌿</span> Suitable Environment</summary>
            <div class="accordion-content">${b.environment || '—'}</div>
          </details>
          <details class="accordion-details accordion-item">
            <summary class="accordion-summary"><span class="emoji">⚕️</span> Common Diseases</summary>
            <div class="accordion-content">${b.diseases || '—'}</div>
          </details>
          <details class="accordion-details accordion-item">
            <summary class="accordion-summary"><span class="emoji">🛡️</span> Treatment and Prevention</summary>
            <div class="accordion-content">${b.treatment || '—'}</div>
          </details>
        </div>
      `;
    }
  }
  // Breed page loader: pages/breed.html
  (function initBreedPage() {
    const isBreedPage = document.querySelector('[data-page="breed"]');
    if (!isBreedPage) return;
    const params = new URLSearchParams(window.location.search);
    const type = params.get('type');
    const name = params.get('name');
    const root = document.getElementById('breed-sections');
    const title = document.getElementById('breed-title');
    const back = document.getElementById('breed-back');
    const heroImg = document.getElementById('breed-img-large');
    const crumbType = document.getElementById('crumb-type');
    const crumbBreed = document.getElementById('crumb-breed');
    const body = document.body;

    body.classList.remove('theme-dairy','theme-poultry','theme-pisciculture','theme-apiculture','theme-sericulture');
    if (type === 'dairy') body.classList.add('theme-dairy');
    else if (type === 'poultry') body.classList.add('theme-poultry');
    else if (type === 'pisciculture') body.classList.add('theme-pisciculture');
    else if (type === 'apiculture') body.classList.add('theme-apiculture');
    else if (type === 'sericulture') body.classList.add('theme-sericulture');
    if (back && type) back.href = `/${type}`;
    if (crumbType && type) {
      const typeLabel = type === 'dairy' ? 'Dairy Farming'
        : type === 'poultry' ? 'Poultry Farming'
        : type === 'pisciculture' ? 'Pisciculture'
        : type === 'apiculture' ? 'Apiculture'
        : type === 'sericulture' ? 'Sericulture' : 'Farming';
      crumbType.textContent = typeLabel;
      crumbType.href = `/${type}`;
    }

    if (!type || !name || !breedsData[type] || !breedsData[type][name]) {
      if (title) title.textContent = 'Not Found';
      if (root) root.innerHTML = '<p>Breed not found. Please go back and select again.</p>';
      return;
    }
    const data = breedsData[type][name];
    if (title) title.textContent = name;
    if (crumbBreed) crumbBreed.textContent = name;
    if (heroImg) {
      const src = '../' + data.image;
      heroImg.src = src;
      heroImg.onload = () => { heroImg.classList.add('is-ready'); };
    }
    if (root) {
      root.innerHTML = `
        <div class="breed-header">
          <img class="breed-photo" src="${'../' + data.image}" alt="${name}" onload="this.classList.add('is-ready')" />
          <div>
            <h3 style="margin: 0 0 2px; font-size: 20px;">${name}</h3>
            <p style="margin: 0; color: var(--muted);">Comprehensive details</p>
          </div>
        </div>
        <div class="accordion">
          <details class="accordion-details accordion-item" open>
            <summary class="accordion-summary"><span class="emoji">📘</span> General Information</summary>
            <div class="accordion-content">${data.info || '—'}</div>
          </details>
          <details class="accordion-details accordion-item">
            <summary class="accordion-summary"><span class="emoji">🥕</span> Food and Nutrition</summary>
            <div class="accordion-content">${data.food || '—'}</div>
          </details>
          <details class="accordion-details accordion-item">
            <summary class="accordion-summary"><span class="emoji">🧼</span> Care</summary>
            <div class="accordion-content">${data.care || '—'}</div>
          </details>
          <details class="accordion-details accordion-item">
            <summary class="accordion-summary"><span class="emoji">🌿</span> Suitable Environment</summary>
            <div class="accordion-content">${data.environment || '—'}</div>
          </details>
          <details class="accordion-details accordion-item">
            <summary class="accordion-summary"><span class="emoji">⚕️</span> Common Diseases</summary>
            <div class="accordion-content">${data.diseases || '—'}</div>
          </details>
          <details class="accordion-details accordion-item">
            <summary class="accordion-summary"><span class="emoji">🛡️</span> Treatment and Prevention</summary>
            <div class="accordion-content">${data.treatment || '—'}</div>
          </details>
        </div>
      `;
    }
  })();
});

