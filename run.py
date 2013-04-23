from app import pcb, db

if __name__ == '__main__':
  db.create_all()
  pcb.run(debug=True)
