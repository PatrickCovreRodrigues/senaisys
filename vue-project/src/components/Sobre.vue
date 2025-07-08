<template>
  <main class="main-content">
    <div class="container">
      <h1 class="page-title">Sobre</h1>
      <p class="page-description">
        Sistema de gerenciamento de cursos SENAI.<br>
        Esta aplicação permite cadastrar e gerenciar cursos técnicos.
      </p>
    </div>
  </main>
</template>

<style scoped>
.main-content {
  padding: 4rem 4rem;
  min-height: calc(100vh - 120px);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  margin: 0;
  background-color: #E8E7E7;
}

.container {
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  text-align: center;
  background-color: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.page-title {
  font-size: 3.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 2rem;
  line-height: 1.2;
}

.page-description {
  font-size: 1.2rem;
  color: #666;
  line-height: 1.6;
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
}

/* Responsive design - Mobile */
@media (max-width: 768px) {
  .main-content {
    padding: 2rem 1rem;
    min-height: calc(100vh - 140px);
  }

  .container {
    padding: 1.5rem;
  }

  .page-title {
    font-size: 2.5rem;
    margin-bottom: 1.5rem;
  }

  .page-description {
    font-size: 1rem;
  }
}

/* Small mobile */
@media (max-width: 480px) {
  .page-title {
    font-size: 2rem;
  }
}
</style> 