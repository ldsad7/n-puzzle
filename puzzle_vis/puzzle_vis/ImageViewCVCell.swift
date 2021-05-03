//
//  ImageViewCVCell.swift
//  puzzle_vis
//
//  Created by Thrynn Simonis on 5/3/21.
//  Copyright © 2021 Thrynn Simonis. All rights reserved.
//

import UIKit

class ImageViewCVCell: UICollectionViewCell {
    
    override init(frame: CGRect) {
        super.init(frame: frame)
        setupViews()
    }
    
    func setupViews() {
        self.addSubview(imgView)
        imgView.leftAnchor.constraint(equalTo: self.leftAnchor).isActive=true
        imgView.topAnchor.constraint(equalTo: self.topAnchor).isActive=true
        imgView.rightAnchor.constraint(equalTo: self.rightAnchor).isActive=true
        imgView.bottomAnchor.constraint(equalTo: self.bottomAnchor).isActive=true
        
        self.addSubview(border)
        border.leftAnchor.constraint(equalTo: self.leftAnchor, constant: 0).isActive=true
        border.topAnchor.constraint(equalTo: self.topAnchor, constant: 0).isActive=true
        border.rightAnchor.constraint(equalTo: self.rightAnchor, constant: 0).isActive=true
        border.bottomAnchor.constraint(equalTo: self.bottomAnchor, constant: 0).isActive=true
        border.isHidden=false
    }
    
    let imgView: UIImageView = {
        let v=UIImageView()
        v.image = ViewController.imageWith(num: 0)!
        v.contentMode = .scaleAspectFit
        v.translatesAutoresizingMaskIntoConstraints=false
        return v
    }()
    
    let border: UIView = {
        let v=UIView()
        v.backgroundColor = UIColor.clear
        v.layer.borderColor = UIColor(red: 11/255, green: 104/255, blue: 250/255, alpha: 0.6).cgColor
        v.layer.borderWidth = 5
        v.translatesAutoresizingMaskIntoConstraints=false
        return v
    }()
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
}
