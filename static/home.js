const $cupcakeList = $('#cupcake-list');
const $newCupcakeForm = $('#new-cupcake-form');
const $addCupcakeButton = $('#new-cupcake-submit');
const $flavorInput = $('#flavor');
const $sizeInput = $('#size');
const $ratingInput = $('#rating');
const $imageInput = $('#image');

$addCupcakeButton.click(addCupcake);

async function addCupcake(evt) {
  evt.preventDefault();
  const cupcakeObj = {
    flavor: $flavorInput.val(),
    size: $sizeInput.val(),
    rating: $ratingInput.val(),
    image: $imageInput.val()
  }
  await postCupcakeToApi(cupcakeObj);
  addCupcakeToPage(cupcakeObj);
  $newCupcakeForm.trigger("reset");
}

async function postCupcakeToApi(cupcake) {
  await axios.post('/api/cupcakes', cupcake);
}

function addCupcakeToPage(cupcake) {
  if (!cupcake.image) {
    cupcake.image = "https://tinyurl.com/demo-cupcake";
  }
  $cupcakeList.append(`
  <figure>
    <h3>${firstCharToUppercase(cupcake.flavor)}:</h3>
    <img class="cupcake-img" src="${cupcake.image}"></img>
  </figure>
`)
}

async function populateCupcakeList() {
  const cupcakes = await axios.get('/api/cupcakes');
  for (const cupcake of cupcakes.data.cupcakes) {
    addCupcakeToPage(cupcake);
  }
}

function firstCharToUppercase(word) {
  return word[0].toUpperCase() + word.substr(1);
}

// on page load
populateCupcakeList();

