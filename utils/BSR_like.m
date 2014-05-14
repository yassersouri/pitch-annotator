function BSR_like
    clear all
    groundTruthPass = '/Users/Azadeh/Desktop/edge/Azadi_S_A/groundTruth';
    train = 'train';
    val = 'val';

    train_dir = sprintf('%s/%s/', groundTruthPass, train);
    val_dir = sprintf('%s/%s/', groundTruthPass, val);
    
    iterate_dir(train_dir);
    iterate_dir(val_dir);
end

function iterate_dir(dir_name)
    files = dir(sprintf('%s*.mat', dir_name));

    for file = files'
        file_name = sprintf('%s%s', dir_name, file.name);
        S = load(file_name);
        groundTruth = create_gt(S.segs, S.edge);
        save(file_name, 'groundTruth');
    end
end

function groundTruth = create_gt(segs, edge)
    groundTruth = {1};
    segs = segs + 1;
    segs = uint16(segs);
    edge = logical(edge);
    groundTruth{1}.Segmentation = segs;
    groundTruth{1}.Boundaries = edge;
end