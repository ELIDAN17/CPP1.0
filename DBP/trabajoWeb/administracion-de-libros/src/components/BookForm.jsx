// src/components/BookForm.jsx
import React, { useState, useEffect, useContext } from 'react';
import { Form, Button } from 'react-bootstrap';
import { BooksContext } from '../context/BooksContext';
// Cambio en la importación para v6: useNavigate en lugar de useHistory
import { useNavigate, useParams } from 'react-router-dom';

function BookForm() {
  const { books, addBook, editBook } = useContext(BooksContext);
  const navigate = useNavigate(); // Hook para la navegación en v6
  const { id } = useParams(); // Para obtener el ID del libro si estamos editando

  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [isbn, setIsbn] = useState('');

  useEffect(() => {
    if (id) {
      const bookToEdit = books.find((book) => book.id === id);
      if (bookToEdit) {
        setTitle(bookToEdit.title);
        setAuthor(bookToEdit.author);
        setIsbn(bookToEdit.isbn);
      }
    }
  }, [id, books]);

  const handleSubmit = (e) => {
    e.preventDefault();

    const newBook = { title, author, isbn };

    if (id) {
      editBook({ ...newBook, id });
    } else {
      addBook(newBook);
    }

    navigate('/'); // Redirigir a la lista de libros con useNavigate
  };

  return (
    <div>
      <h2>{id ? 'Edit Book' : 'Add New Book'}</h2>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Title</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Author</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter author"
            value={author}
            onChange={(e) => setAuthor(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>ISBN</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter ISBN"
            value={isbn}
            onChange={(e) => setIsbn(e.target.value)}
            required
          />
        </Form.Group>

        <Button variant="primary" type="submit">
          {id ? 'Update Book' : 'Add Book'}
        </Button>
        {' '}
        <Button variant="secondary" onClick={() => navigate('/')}> {/* Usar navigate para Cancel */}
          Cancel
        </Button>
      </Form>
    </div>
  );
}

export default BookForm;