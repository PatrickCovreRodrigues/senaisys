<template>
  <header class="navbar">
    <div class="navbar-brand">
      <button class="logo-btn" @click="voltarHome" aria-label="Voltar para Home">
        <img src="@/assets/senailogo.png" alt="SESI SENAI" class="brand-logo" />
      </button>
    </div>
    <nav class="navbar-menu">
      <router-link to="/novo-cadastro" class="nav-link">Novo cadastro</router-link>
      <router-link to="/meus-cadastros" class="nav-link">Meus Cadastros</router-link>
      <router-link to="/sobre" class="nav-link">Sobre</router-link>
    </nav>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const voltarHome = () => {
  router.push('/')
}
</script>

<style scoped>
.navbar {
  background-color: white;
  padding: 1.5rem 4rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 100;
  width: 100%;
  margin: 0;
}

.navbar-brand .brand-logo {
  height: 40px;
  width: auto;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.navbar-brand .brand-logo:hover {
  transform: scale(1.05);
}

.navbar-menu {
  display: flex;
  gap: 3rem;
}

.nav-link {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  font-size: 1.1rem;
  transition: color 0.3s ease;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
}

.nav-link:hover {
  color: #4F46E5;
  background-color: rgba(79, 70, 229, 0.1);
}

.nav-link.router-link-active {
  color: #4F46E5;
  background-color: rgba(79, 70, 229, 0.1);
}

.logo-btn {
  background: none;
  border: none;
  padding: 0;
  margin: 0;
  cursor: pointer;
  outline: none;
}
.logo-btn:focus {
  outline: none;
}

/* Responsive design - Tablet */
@media (max-width: 1024px) {
  .navbar {
    padding: 1.5rem 2rem;
  }
}

/* Responsive design - Mobile */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    gap: 1.5rem;
    padding: 1.5rem;
  }

  .navbar-menu {
    gap: 1.5rem;
    flex-wrap: wrap;
    justify-content: center;
  }

  .nav-link {
    font-size: 1rem;
  }
  
  .navbar-brand .brand-logo {
    height: 35px;
  }
}
</style>