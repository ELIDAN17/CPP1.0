// src/context/BooksContext.jsx
import React, { createContext, useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid'; // Necesitamos 'uuid' para IDs únicos
import _ from 'lodash'; // Necesitamos 'lodash' para algunas operaciones

// 1. Crear el Contexto
export const BooksContext = createContext();

// 2. Crear el Proveedor del Contexto
const BooksContextProvider = (props) => {
  // Estado para la lista de libros
  const [books, setBooks] = useState(() => {
    // Intentar cargar libros desde localStorage al inicio
    const localData = localStorage.getItem('books');
    return localData ? JSON.parse(localData) : [];
  });

  // Efecto para guardar los libros en localStorage cada vez que cambien
  useEffect(() => {
    localStorage.setItem('books', JSON.stringify(books));
  }, [books]);

  // Función para agregar un libro
  const addBook = (book) => {
    setBooks([...books, { ...book, id: uuidv4() }]);
  };

  // Función para eliminar un libro
  const deleteBook = (id) => {
    setBooks(books.filter((book) => book.id !== id));
  };

  // Función para editar un libro
  const editBook = (updatedBook) => {
    setBooks(
      books.map((book) => (book.id === updatedBook.id ? updatedBook : book))
    );
  };

  // El valor que se proporcionará a los consumidores del contexto
  const contextValue = {
    books,
    addBook,
    deleteBook,
    editBook,
  };

  return (
    <BooksContext.Provider value={contextValue}>
      {props.children}
    </BooksContext.Provider>
  );
};

export default BooksContextProvider;