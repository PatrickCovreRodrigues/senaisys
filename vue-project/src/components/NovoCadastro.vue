<template>
  <main class="main-content">
    <div class="container">
      <h1 class="page-title">Novo Cadastro</h1>
      
      <div class="cards-grid">
        <div class="card" @click="openSection('curso')">
          <div class="card-icon">C</div>
          <div class="card-label">Curso</div>
        </div>
        
        <div class="card" @click="openSection('uc')">
          <div class="card-icon">U</div>
          <div class="card-label">UC</div>
        </div>
        
        <div class="card" @click="openSection('docentes')">
          <div class="card-icon">D</div>
          <div class="card-label">Docentes</div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

// Function to handle card clicks
const openSection = (section) => {
  console.log(`Opening ${section} section for new registration`)
  
  if (section === 'curso') {
    // Navegar para formulário de novo curso
    router.push('/criar-curso-form')
  } else if (section === 'uc') {
    // Navegar para formulário de nova UC
    router.push('/criar-uc-form')
  } else if (section === 'docentes') {
    // Navegar para formulário de novo docente
    router.push('/criar-docente-form')
  }
}
</script>

<style scoped>
.main-content {
  padding: 4rem 4rem;
  min-height: calc(100vh - 120px);
  width: 100%;
  margin: 0;
  background-color: #E8E7E7;
}

.container {
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  background-color: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.page-title {
  font-size: 3.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 4rem;
  text-align: left;
}

.cards-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  max-width: 900px;
  width: 100%;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 2.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  min-height: 120px;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  border-color: #4F46E5;
}

.card-icon {
  width: 50px;
  height: 50px;
  background-color: #9CA3AF;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  border-radius: 8px;
  flex-shrink: 0;
}

.card-label {
  font-size: 1.2rem;
  font-weight: 500;
  color: #333;
}

/* Responsive design - Tablet */
@media (max-width: 1024px) {
  .main-content {
    padding: 3rem 2rem;
  }
  
  .container {
    padding: 2rem;
  }
  
  .page-title {
    font-size: 3rem;
  }
  
  .cards-grid {
    max-width: 700px;
    gap: 1.5rem;
  }
  
  .card {
    padding: 2rem;
    min-height: 100px;
  }
}

/* Responsive design - Mobile */
@media (max-width: 768px) {
  .main-content {
    padding: 2rem 1rem;
  }

  .container {
    padding: 1.5rem;
  }

  .page-title {
    font-size: 2.5rem;
    margin-bottom: 3rem;
    text-align: center;
  }
  
  .cards-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
    max-width: 100%;
  }
  
  .card {
    padding: 1.5rem;
    min-height: 80px;
  }
}

/* Small mobile */
@media (max-width: 480px) {
  .page-title {
    font-size: 2rem;
  }
  
  .card {
    padding: 1rem;
    gap: 1rem;
    min-height: 70px;
  }
  
  .card-icon {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
  }
  
  .card-label {
    font-size: 1rem;
  }
}
</style> 