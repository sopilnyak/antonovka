<template>
  <div>
    <div id="header">
      Проверьте свою яблоню
    </div>
    <div id="subheader">
      Загрузите фото листа и узнайте, болеет ли ваша яблоня
    </div>
    <div id="app">
      <Root />
    </div>
  </div>
</template>

<script>
import Root from "./components/Root.vue";

export default {
  name: "app",
  components: {
    Root,
  },
};
</script>

<style>
body {
  background: #134e5e;
  background: -webkit-linear-gradient(to left, #71b280, #134e5e);
  background: linear-gradient(to left, #71b280, #134e5e);
  font-family: "Segoe UI", "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-width: 30em;
}

#header {
  color: #fff;
  margin-left: 50px;
  font-size: 3.5em;
}

#subheader {
  color: rgba(255, 255, 255, 0.781);
  margin-left: 55px;
  margin-top: 0.5em;
  font-size: 1.4em;
}

#app {
  background-color: #fff;
  margin: 50px;
  min-height: 78vh;
  margin-bottom: 0;
  border: 1px #535c68 solid;
  box-shadow: 0px 0px 33px -7px #1e272e;
  text-align: center;
  margin-top: 1.5em;
  min-width: 30em;
}
</style>
