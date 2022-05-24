<template>
  <main id="about-page">
    <div id="left">
      <div id="about-page-info">
        <h1>About Fuel Guru</h1>  
        <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Placeat ipsum similique, accusantium ex vero alias quia temporibus nisi eos neque? Pariatur assumenda eligendi iusto cumque nam debitis, explicabo deserunt! Aliquid expedita iusto recusandae officia vel saepe blanditiis enim amet impedit. Odio, suscipit inventore, ducimus accusamus fugiat unde dicta esse ad quisquam, nisi animi culpa maiores dignissimos quas repellendus eveniet dolorum quidem debitis placeat? Aperiam beatae maxime, laborum veniam molestiae nam fuga aliquam similique eos voluptatem labore officia. Eius accusamus sapiente autem atque quaerat alias, nobis delectus? Repudiandae labore, mollitia culpa provident veritatis consectetur laborum sunt error ipsum, alias ipsam sequi.</p>
        <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Placeat ipsum similique, accusantium ex vero alias quia temporibus nisi eos neque? Pariatur assumenda eligendi iusto cumque nam debitis, explicabo deserunt! Aliquid expedita iusto recusandae officia vel saepe blanditiis enim amet impedit. Odio, suscipit inventore, ducimus accusamus fugiat unde dicta esse ad quisquam, nisi animi culpa maiores dignissimos quas repellendus eveniet dolorum quidem debitis placeat? Aperiam beatae maxime, laborum veniam molestiae nam fuga aliquam similique eos voluptatem labore officia. Eius accusamus sapiente autem atque quaerat alias, nobis delectus? Repudiandae labore, mollitia culpa provident veritatis consectetur laborum sunt error ipsum, alias ipsam sequi.</p>
      </div>
      <div id="about-page-btn">
        <router-link :to="{name: 'Signup'}" id="home-page-btn">Signup Today!</router-link>
        <router-view/>
      </div>
    </div>
  </main>
</template>

<style>
  #about-page-btn {
    padding-top: 30px; 
  }
</style>
