import Vue from 'vue'
import App from './App.vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faPlus } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import VTooltip from 'v-tooltip'

Vue.config.productionTip = false

Vue.component("font-awesome-icon", FontAwesomeIcon);
library.add(faPlus)
Vue.use(VTooltip)

new Vue({
  render: h => h(App),
}).$mount('#app')
