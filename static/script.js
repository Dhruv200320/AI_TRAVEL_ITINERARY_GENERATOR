function navigateTo(sectionId) {
  const section = document.getElementById(sectionId);
  if (section) {
    section.scrollIntoView({ behavior: "smooth" });
  }
}

function submitForm(event) {
  event.preventDefault();
  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const message = document.getElementById("message").value.trim();
  if (name && email && message) {
    alert(`Thank you, ${name}! Your message has been received.`);
    event.target.reset();
  }
}

const indianTours = [
  {
    title: "Kashmir",
    img: "https://media.istockphoto.com/id/532959840/photo/gulmarg-high-peaks.jpg?s=612x612&w=0&k=20&c=WP0MGH2QBSzAqrtYG4Ryr17303VkwoCfkONyjiruo7I=",
    text: "Snow-capped mountains and shikara rides."
  },
  {
    title: "Goa",
    img: "https://media.istockphoto.com/id/157579910/photo/the-beach.jpg?s=612x612&w=0&k=20&c=aMk67AmzIVD_S1Nibww8ytUdyub2ck3HNQ3uTvuPWPI=",
    text: "Beaches, parties, and Portuguese heritage."
  },
  {
    title: "Rajasthan",
    img: "https://st2.depositphotos.com/1000528/7802/i/450/depositphotos_78020736-stock-photo-two-cameleers-camel-drivers-with.jpg",
    text: "Palaces, deserts, and royal legacy."
  },
  {
    title: "Kerala",
    img: "https://media.istockphoto.com/id/1246366598/photo/a-scenic-view-of-boats-under-a-blue-sky-in-backwaters-situated-in-allepey-town-located-in.jpg?s=612x612&w=0&k=20&c=YBv_3nP-6YjvN9JRhaNsBmq8ke4azCgvGLS5h3r9jSk=",
    text: "Backwaters, greenery, and houseboats."
  }
];

const internationalTours = [
  {
    title: "Paris",
    img: "https://media.istockphoto.com/id/1498516775/photo/the-eiffel-tower-in-paris-france-at-sunset.jpg?s=612x612&w=0&k=20&c=V4StdESr6-QQWOjXm6R8b1T-_slWLxasMnN6SWdV9ko=",
    text: "Eiffel Tower, cafes, and romance."
  },
  {
    title: "Bali",
    img: "https://media.istockphoto.com/id/675172642/photo/pura-ulun-danu-bratan-temple-in-bali.jpg?s=612x612&w=0&k=20&c=_MPdmDviIyhldqhf7t6s63C-bZbTGfNHMlJP9SIa8Y0=",
    text: "Beaches, temples, and island vibes."
  },
  {
    title: "New York",
    img: "https://media.gettyimages.com/id/533998713/photo/empire-state-building-at-night.jpg?s=612x612&w=gi&k=20&c=3DbVKyYa3uHn9NCRCUMasBy4ju4sBsuppHfdE1zTP3s=",
    text: "Skyscrapers, Times Square, and Broadway."
  },
  {
    title: "Dubai",
    img: "https://media.istockphoto.com/id/154918211/photo/city-of-dubai-burj-khalifa.jpg?s=612x612&w=0&k=20&c=IQ1upJGlnISqrBcBpmDS8HTCw-u6j08GkrFwV2QEMQk=",
    text: "Luxury shopping, Burj Khalifa, and desert safaris."
  }
];

function createCard({ title, img, text }) {
  return `
    <div class="col-md-4 col-lg-3">
      <div class="card h-100">
        <img src="${img}" class="card-img-top" alt="${title}">
        <div class="card-body">
          <h5 class="card-title">${title}</h5>
          <p class="card-text">${text}</p>
          <button class="btn btn-sm btn-teal" onclick="viewDetails('${title}')">View Details</button>
        </div>
      </div>
    </div>`;
}

function renderTours() {
  document.getElementById("india-tours").innerHTML = indianTours.map(createCard).join("");
  document.getElementById("world-tours").innerHTML = internationalTours.map(createCard).join("");
}

function filterTours(query) {
  const search = query.toLowerCase();
  const indiaFiltered = indianTours.filter(tour => tour.title.toLowerCase().includes(search));
  const worldFiltered = internationalTours.filter(tour => tour.title.toLowerCase().includes(search));
  document.getElementById("india-tours").innerHTML = indiaFiltered.map(createCard).join("");
  document.getElementById("world-tours").innerHTML = worldFiltered.map(createCard).join("");
}

function viewDetails(title) {
  alert(`Here's more information about ${title}!`);
}

window.onload = renderTours;
