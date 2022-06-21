<template>
  <main id="home-page">
    <div id="left">
      <div id="left-heading">
        <h1>Welcome to <br> Fuel Guru</h1>    
      </div>    
      <div id="left-paragraph">
        <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Placeat ipsum similique, accusantium ex vero alias quia temporibus nisi eos neque? Pariatur assumenda eligendi iusto cumque nam debitis, explicabo deserunt! Aliquid expedita iusto recusandae officia vel saepe blanditiis enim amet impedit. Odio, suscipit inventore, ducimus accusamus fugiat unde dicta esse ad quisquam, nisi animi culpa maiores dignissimos quas repellendus eveniet dolorum quidem debitis placeat? Aperiam beatae maxime, laborum veniam molestiae nam fuga aliquam similique eos voluptatem labore officia. Eius accusamus sapiente autem atque quaerat alias, nobis delectus? Repudiandae labore, mollitia culpa provident veritatis consectetur laborum sunt error ipsum, alias ipsam sequi.</p>
      </div>
      <div id="left-button">
        <router-link :to="{name: 'Login'}" id="home-page-btn">Signup / Login</router-link>
        <router-view/>
      </div>
    </div>
    <div id="right">
      <img src="@/assets/home_image1.jpg" alt="Fuel Guru Image" id="home-img">
    </div>
  </main>
</template>

<style>
  #home-page {
    display: grid;
    grid-template-columns: auto auto;
    column-gap: 160px;
  }

  #left {
    text-align: left;
  }

  h1 {
    font-size: 60px;
    text-align: left;
  }

  #home-page-btn {
    border: 2px solid #AA1414;
    border-radius: 25px;
    padding-top: 5px;
    padding-bottom: 5px;
    padding-left: 20px;
    padding-right: 20px;
    background-color: #AA1414;
    color: white;
  }

  #left-button {
    padding-top: 30px;
  }

  #home-img {
    height: 80%;
  }
</style>