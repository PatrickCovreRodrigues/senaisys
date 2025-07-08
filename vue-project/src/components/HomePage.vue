<template>
  <main class="main-content">
    <div class="container">
      <div class="welcome-section">
        <h1 class="welcome-title">Bem-vindo ao Sistema SENAI</h1>
        <p class="welcome-subtitle">Gerencie seus cursos, unidades curriculares e docentes de forma eficiente</p>
        
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">📚</div>
            <h3>Cursos</h3>
            <p>Organize e gerencie todos os seus cursos técnicos</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3>Unidades Curriculares</h3>
            <p>Controle as disciplinas e carga horária</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">👥</div>
            <h3>Docentes</h3>
            <p>Gerencie professores e suas especialidades</p>
          </div>
        </div>
        
        <div class="cta-section" @click="gerarCalendario">
          <div class="cta-icon">📅</div>
          <p class="cta-text">Clique aqui para gerar um calendário escolar</p>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const gerarCalendario = () => {
  router.push('/gerar-calendario')
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
  padding: 4rem 3rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.welcome-section {
  text-align: center;
  max-width: 1000px;
  margin: 0 auto;
}

.welcome-title {
  font-size: 3.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.welcome-subtitle {
  font-size: 1.3rem;
  color: #666;
  margin-bottom: 4rem;
  line-height: 1.6;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 4rem;
}

.feature-card {
  background: #f8fafc;
  border-radius: 12px;
  padding: 2.5rem;
  text-align: center;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border-color: #4F46E5;
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}

.cta-section {
  background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
  border-radius: 12px;
  padding: 2rem;
  color: white;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.cta-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(79, 70, 229, 0.4);
}

.cta-icon {
  font-size: 2rem;
}

.cta-text {
  font-size: 1.1rem;
  margin: 0;
  line-height: 1.6;
}

/* Responsive design - Tablet */
@media (max-width: 1024px) {
  .main-content {
    padding: 3rem 2rem;
  }
  
  .container {
    padding: 3rem 2rem;
  }
  
  .welcome-title {
    font-size: 3rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .feature-card {
    padding: 2rem;
  }
}

/* Responsive design - Mobile */
@media (max-width: 768px) {
  .main-content {
    padding: 2rem 1rem;
  }

  .container {
    padding: 2rem 1.5rem;
  }

  .welcome-title {
    font-size: 2.5rem;
    margin-bottom: 1rem;
  }
  
  .welcome-subtitle {
    font-size: 1.1rem;
    margin-bottom: 3rem;
  }
  
  .features-grid {
    margin-bottom: 3rem;
  }
  
  .feature-card {
    padding: 1.5rem;
  }
  
  .feature-icon {
    font-size: 2.5rem;
  }
  
  .feature-card h3 {
    font-size: 1.3rem;
  }
}

/* Small mobile */
@media (max-width: 480px) {
  .welcome-title {
    font-size: 2rem;
  }
  
  .welcome-subtitle {
    font-size: 1rem;
  }
  
  .feature-card {
    padding: 1rem;
  }
  
  .feature-icon {
    font-size: 2rem;
  }
  
  .feature-card h3 {
    font-size: 1.2rem;
  }
  
  .cta-text {
    font-size: 1rem;
  }
}
</style> 