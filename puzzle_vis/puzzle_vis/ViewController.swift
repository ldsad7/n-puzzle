//
//  ViewController.swift
//  puzzle_vis
//
//  Created by Thrynn Simonis on 5/3/21.
//  Copyright © 2021 Thrynn Simonis. All rights reserved.
//

import UIKit

extension UIButton {
    private func actionHandle(action:(() -> Void)? = nil) {
        struct __ { static var action :(() -> Void)? }
        if action != nil { __.action = action }
        else { __.action?() }
    }
    @objc private func triggerActionHandler() {
        self.actionHandle()
    }
    func actionHandle(controlEvents control :UIControl.Event, ForAction action:@escaping () -> Void) {
        self.actionHandle(action: action)
        self.addTarget(self, action: #selector(triggerActionHandler), for: control)
    }
}

class ViewController: UIViewController, UICollectionViewDelegate, UICollectionViewDataSource, UICollectionViewDelegateFlowLayout {
    
    var size = 4
    var numberOfSteps = 0
    
    var startIntArray = [Int]()
    var currentIntArray = [Int]()
    var finalIntArray = [Int]()
    var currentImageArray=[UIImage]()
    
    var movesArray = [(first: IndexPath, second: IndexPath)]()
    var moveIndex = 0
    
    static func imageWith(num: Int) -> UIImage? {
        let frame = CGRect(x: 0, y: 0, width: 100, height: 100)
        let nameLabel = UILabel(frame: frame)
        nameLabel.textAlignment = .center
        nameLabel.backgroundColor = .green
        nameLabel.textColor = .red
        nameLabel.font = UIFont.boldSystemFont(ofSize: 40)
        if num != 0 {
            nameLabel.text = String(num)
        }
        UIGraphicsBeginImageContext(frame.size)
        if let currentContext = UIGraphicsGetCurrentContext() {
            nameLabel.layer.render(in: currentContext)
            let nameImage = UIGraphicsGetImageFromCurrentImageContext()
            return nameImage
        }
        return nil
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.title = "N-Puzzle"
        self.navigationController?.navigationBar.isTranslucent = false

        // get size, start arr, final arr, list of swaps
        
        // TODO: replace this part of code from `python n_puzzle.py -s ...`
        size = 4
        startIntArray = [0, 13, 14, 5, 2, 3, 4, 1, 6, 12, 10, 15, 7, 9, 11, 8]
        finalIntArray = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
        let inputMovesArray = [(0, 1), (1, 2), (2, 6), (6, 7), (7, 3), (3, 2), (2, 6), (6, 5), (5, 1), (1, 2), (2, 6), (6, 7), (7, 11), (11, 15), (15, 14), (14, 10), (10, 9), (9, 5), (5, 4), (4, 0), (0, 1), (1, 5), (5, 6), (6, 10), (10, 9), (9, 8), (8, 4), (4, 5), (5, 9), (9, 13), (13, 12), (12, 8), (8, 9), (9, 13), (13, 14), (14, 10), (10, 11), (11, 7), (7, 6), (6, 10), (10, 9), (9, 13), (13, 14), (14, 15), (15, 11), (11, 7), (7, 6), (6, 10), (10, 14), (14, 15)]

        currentIntArray = startIntArray
        movesArray = []
        for group in inputMovesArray {
            let (left, right) = group
            movesArray.append((IndexPath(row: left, section: 0), IndexPath(row: right, section: 0)))
        }

        currentImageArray = []
        for num in currentIntArray {
            currentImageArray.append(ViewController.imageWith(num: num)!)
        }

        setupViews()
    }

    @objc func btnPlayAction() {
        while self.moveIndex < self.movesArray.count {
            self.btnSwapAction()
        }
    }

    @objc func btnSwapAction() {
        if self.moveIndex >= self.movesArray.count {
            self.checkIsSolved()
            return
        }
        let (start, end) = self.movesArray[self.moveIndex]
        myCollectionView.performBatchUpdates({
            myCollectionView.moveItem(at: start, to: end)
            myCollectionView.moveItem(at: end, to: start)
        })
        self.myCollectionView.deselectItem(at: start, animated: true)
        self.myCollectionView.deselectItem(at: end, animated: true)
        self.currentImageArray.swapAt(start.item, end.item)
        self.currentIntArray.swapAt(start.item, end.item)
        self.checkIsSolved()
        self.numberOfSteps += 1
        self.moveIndex += 1
        self.lblMoves.text = "Number of steps: \(self.numberOfSteps)"
    }

    @objc func btnUndoAction() {
        if self.moveIndex <= 0 {
            self.checkIsSolved()
            return
        }
        let (start, end) = movesArray[moveIndex - 1]
        myCollectionView.performBatchUpdates({
            myCollectionView.moveItem(at: start, to: end)
            myCollectionView.moveItem(at: end, to: start)
        })
        self.currentImageArray.swapAt(start.item, end.item)
        self.currentIntArray.swapAt(start.item, end.item)
        self.moveIndex -= 1
        self.numberOfSteps -= 1
        self.lblMoves.text = "Number of steps: \(self.numberOfSteps)"
        self.checkIsSolved()
    }

    func checkIsSolved() {
        if self.currentIntArray == self.finalIntArray {
            let alert=UIAlertController(title: "Info", message: "Puzzle is solved 👍", preferredStyle: .alert)
            let okAction = UIAlertAction(title: "OK", style: .default, handler: nil)
            let restartAction = UIAlertAction(title: "Restart", style: .default, handler: { (action) in
                self.restartGame()
            })
            alert.addAction(okAction)
            alert.addAction(restartAction)
            self.present(alert, animated: true, completion: nil)
        }
    }

    func restartGame() {
        currentIntArray = startIntArray
        currentImageArray = []
        for num in currentIntArray {
            currentImageArray.append(ViewController.imageWith(num: num)!)
        }
        
        self.numberOfSteps = 0
        self.moveIndex = 0
        self.lblMoves.text = "Number of steps: \(numberOfSteps)"
        self.myCollectionView.reloadData()
    }
    
    //MARK: CollectionView
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return size * size
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell=collectionView.dequeueReusableCell(withReuseIdentifier: "Cell", for: indexPath) as! ImageViewCVCell
        cell.imgView.image=currentImageArray[indexPath.item]
        return cell
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
        let width = collectionView.frame.width
        return CGSize(width: width/CGFloat(size), height: width/CGFloat(size))
    }
    
    func setupViews() {
        myCollectionView.delegate=self
        myCollectionView.dataSource=self
        myCollectionView.register(ImageViewCVCell.self, forCellWithReuseIdentifier: "Cell")
        myCollectionView.backgroundColor=UIColor.white
        
        self.view.addSubview(myCollectionView)
        myCollectionView.leftAnchor.constraint(equalTo: self.view.leftAnchor, constant: 20).isActive=true
        myCollectionView.topAnchor.constraint(equalTo: self.view.topAnchor, constant: 50).isActive=true
        myCollectionView.rightAnchor.constraint(equalTo: self.view.rightAnchor, constant: -20).isActive=true
        myCollectionView.heightAnchor.constraint(equalTo: myCollectionView.widthAnchor).isActive=true
        
        self.view.addSubview(btnUndo)
        btnUndo.widthAnchor.constraint(equalToConstant: 175).isActive=true
        btnUndo.heightAnchor.constraint(equalToConstant: 50).isActive=true
        btnUndo.leftAnchor.constraint(equalTo: self.view.leftAnchor).isActive=true
        btnUndo.topAnchor.constraint(equalTo: myCollectionView.bottomAnchor, constant: 20).isActive=true
        btnUndo.addTarget(self, action: #selector(btnUndoAction), for: .touchUpInside)
        
        self.view.addSubview(btnPlay)
        btnPlay.widthAnchor.constraint(equalToConstant: 50).isActive=true
        btnPlay.heightAnchor.constraint(equalToConstant: 50).isActive=true
        btnPlay.centerXAnchor.constraint(equalTo: self.view.centerXAnchor).isActive=true
        btnPlay.topAnchor.constraint(equalTo: myCollectionView.bottomAnchor, constant: 20).isActive=true
        btnPlay.addTarget(self, action: #selector(btnPlayAction), for: .touchUpInside)
        
        self.view.addSubview(btnSwap)
        btnSwap.widthAnchor.constraint(equalToConstant: 175).isActive=true
        btnSwap.heightAnchor.constraint(equalToConstant: 50).isActive=true
        btnSwap.topAnchor.constraint(equalTo: myCollectionView.bottomAnchor, constant: 20).isActive=true
        btnSwap.rightAnchor.constraint(equalTo: self.view.rightAnchor).isActive=true
        btnSwap.addTarget(self, action: #selector(btnSwapAction), for: .touchUpInside)
        
        self.view.addSubview(lblMoves)
        lblMoves.widthAnchor.constraint(equalToConstant: 200).isActive=true
        lblMoves.topAnchor.constraint(equalTo: btnUndo.bottomAnchor, constant: 10).isActive=true
        lblMoves.centerXAnchor.constraint(equalTo: self.view.centerXAnchor).isActive=true
        lblMoves.heightAnchor.constraint(equalToConstant: 50).isActive=true
        lblMoves.text = "Number of steps: \(numberOfSteps)"
    }

    let myCollectionView: UICollectionView = {
        let layout = UICollectionViewFlowLayout()
        layout.minimumInteritemSpacing=0
        layout.minimumLineSpacing=0
        let cv = UICollectionView(frame: CGRect.zero, collectionViewLayout: layout)
        cv.allowsMultipleSelection = true
        cv.translatesAutoresizingMaskIntoConstraints=false
        return cv
    }()
    
    let btnUndo: UIButton = {
        let btn=UIButton(type: .system)
        btn.setTitle("Previous", for: .normal)
        btn.setTitleColor(UIColor.blue, for: .normal)
        btn.titleLabel?.font = UIFont.systemFont(ofSize: 20)
        btn.translatesAutoresizingMaskIntoConstraints=false
        return btn
    }()

    let btnPlay: UIButton = {
        let btn=UIButton(type: .system)
        btn.setTitle("▶️", for: .normal)
        btn.titleLabel?.font = UIFont.systemFont(ofSize: 40)
        btn.translatesAutoresizingMaskIntoConstraints=false
        return btn
    }()

    let btnSwap: UIButton = {
        let btn=UIButton() // type: .system
        btn.setTitle("Next", for: .normal)
        btn.setTitleColor(UIColor.blue, for: .normal)
        btn.titleLabel?.font = UIFont.systemFont(ofSize: 20)
        btn.translatesAutoresizingMaskIntoConstraints=false
        return btn
    }()

    let lblMoves: UILabel = {
        let lbl=UILabel()
        lbl.textAlignment = .center
        lbl.textColor = UIColor.red
        lbl.translatesAutoresizingMaskIntoConstraints=false
        return lbl
    }()
}
