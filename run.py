from app import pcb, db

if __name__ == '__main__':
  db.create_all()
<<<<<<< HEAD
=======
  #print pcb.url_map
>>>>>>> de98cfca0e73b3046b41f82af0c4f4c65a263ea4
  pcb.run(debug=True)
