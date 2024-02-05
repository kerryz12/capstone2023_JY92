
export function login(form, loading, email, password) {
    if (!this.form) return
        this.loading = true

    if (this.emailLogin === "test@whms.com" || this.passwordLogin === "testwhms") {
      this.$router.push('/');
    } else {
      tryagain = true;
    }
    this.loading = false

  }

  export function required(v) {
    return !!v || 'Field is required'
  }