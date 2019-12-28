const state = () => ({
  snackbar: {
    show: false,
    color: "pink",
    text: "",
    timeout: 5000,
    right: true,
    bottom: true
  }
})

const getters = {
  getSnackbar: state => state.snackbar
}

const actions = {
  sendError({ commit, state }, text) {
    let snackbar = state.snackbar
    snackbar.show = true
    snackbar.text = text
    snackbar.color = "pink"
    commit('setSnack', snackbar)
  },
  sendSuccess({ commit, state }, text) {
    let snackbar = state.snackbar
    snackbar.show = true
    snackbar.text = text
    snackbar.color = "green"
    commit('setSnack', snackbar)
  },
  closeSnackbar({ commit, state }) {
    let snackbar = state.snackbar
    snackbar.show = false
    commit('setSnack', snackbar)
  }
}

const mutations = {
  setSnack(state, snackbar) {
    state.snackbar = snackbar
  }
}

export default {
  state,
  actions,
  getters,
  mutations
}
