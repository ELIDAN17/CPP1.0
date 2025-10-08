// src/App.jsx
import React from 'react';
// Cambios en la importación de react-router-dom para v6
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Container, Navbar, Nav } from 'react-bootstrap';

import BooksContextProvider from './context/BooksContext';
import BookList from './components/BookList.jsx';
import BookForm from './components/BookForm.jsx';

function App() {
  return (
    <BooksContextProvider>
      <Router>
        <Navbar bg="dark" variant="dark" expand="lg" className="mb-4">
          <Container>
            <Navbar.Brand as={Link} to="/">Book Management App</Navbar.Brand> {/* Navbar.Brand también usa 'as={Link}' */}
            <Nav className="me-auto">
              <Nav.Item>
                <Nav.Link as={Link} to="/">Books</Nav.Link> {/* Nav.Link usa 'as={Link}' */}
              </Nav.Item>
              <Nav.Item>
                <Nav.Link as={Link} to="/add">Add Book</Nav.Link> {/* Nav.Link usa 'as={Link}' */}
              </Nav.Item>
            </Nav>
          </Container>
        </Navbar>

        <Container>
          {/* CAMBIO GRANDE AQUÍ: Routes en lugar de Switch, y element en lugar de component */}
          <Routes>
            {/* La prop 'exact' ya no es necesaria en v6, ya que las rutas son más inteligentes */}
            <Route path="/" element={<BookList />} /> {/* Renderiza BookList directamente */}
            <Route path="/add" element={<BookForm />} /> {/* Renderiza BookForm */}
            <Route path="/edit/:id" element={<BookForm />} /> {/* Renderiza BookForm para edición */}
          </Routes>
        </Container>
      </Router>
    </BooksContextProvider>
  );
}

export default App;